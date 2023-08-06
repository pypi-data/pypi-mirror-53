import os
import re
import csv
import copy
import json
import traceback

import numpy as np
import pandas as pd

from gradefast import utils
from gradefast.exceptions import *

class Result:
    def __init__(self, team_id: int, file: str, result_dict: dict, pkg_path: str = '', comment: str = ''):
        if not isinstance(result_dict, dict):
            raise TypeError("Result should be a dict")

        # identify by team id
        if type(team_id) == str and utils.is_string_number(team_id):
            self.team_id = int(team_id)
        else:
            self.team_id = team_id

        # which file did the test run on?
        self.file = file
        # which package?
        self.pkg_path = pkg_path

        # the real thing
        self.result_dict = result_dict

        self.comment = comment

    def __eq__(self, value):
        if not isinstance(value, Result):
            return False
        if self.team_id != value.team_id:
            return False
        if self.file != value.file:
            return False
        if self.pkg_path != value.pkg_path:
            return False
        if self.result_dict != value.result_dict:
            return False
        if self.comment != value.comment:
            return False
        return True

    def __ne__(self, value):
        return not self.__eq__(value)

    def __repr__(self):
        return "Result(team_id: {}, file: {}, result_dict: {}, pkg_path: {}, comment: {})".format(self.team_id, self.file, self.result_dict, self.pkg_path, self.comment)

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def from_submission_test(submission, test, result, comment=''):
        return Result(submission.team_id, test.file_to_test, result, pkg_path=test.package_path, comment=comment)

    @staticmethod
    def from_dict(result):
        if 'team_id' in result:
            team_id = result['team_id']
        if 'file' in result:
            file = result['file']
        if 'pkg_path' in result:
            pkg_path = result['pkg_path']
        if 'comment' in result:
            comment = result['comment']
        if 'result_dict' in result:
            result_dict = result['result_dict']

        return Result(team_id, file, result_dict, pkg_path, comment)

    def to_dict(self):
        return self.__dict__

    def to_flat_dict(self):
        return {'team_id': self.team_id, 'file': self.file, 'pkg_path': self.pkg_path, **self.result_dict, 'comment': self.comment}

    def flat_result(self, average=True):
        '''
            Flatten result by adding or averaging test cases
        '''
        result_copy = copy.deepcopy(self.result_dict)
        total = 0
        for key, value in result_copy.items():
            if value != np.nan:
                if type(value) == list:
                    result_copy[key] = self._aggregate_test_cases(value, average)
                else:
                    result_copy[key] = value
        return Result(self.team_id, self.file, result_copy, self.pkg_path)

    def add(self, average=True):
        '''
            Aggregates values in result dictionary into a single total field
        '''
        result_copy = copy.deepcopy(self.result_dict)
        total = 0
        for key, value in result_copy.items():
            if value != np.nan:
                if type(value) == list:
                    total += self._aggregate_test_cases(value, average)
                else: 
                    total += value

        return Result(self.team_id, self.file, {'total': total}, self.pkg_path)

    @staticmethod
    def multiply_list(marks, weightage):
        final_marks = []
        for idx, value in enumerate(marks):
            if type(value) not in [int, float]:
                raise Exception('Test cases marks should be numbers')

            if type(weightage) not in [list, int, float]:
                raise Exception('Weightages should be number or list of numbers')

            if type(weightage) == list and (len(weightage) != len(marks)):
                raise Exception('Either specify a single multiplier or all multiplers for weightages')
            elif type(weightage) == list and (len(weightage) == len(marks)):
                result = value * weightage[idx]
            else:
                result = value * weightage
            final_marks.append(result)
        return final_marks


    def multiply(self, weightages):
        '''
            Multiply result with weightages to transform a resutlt appropriately
        '''
        result_copy = copy.deepcopy(self.result_dict)
        total = 0
        for param, marks in self.result_dict.items():
            if param not in weightages:
                continue
            if marks != np.nan:
                if type(marks) == list:
                    result_copy[param] = Result.multiply_list(marks, weightages[param])
                elif type(marks) in [int, float] and type(weightages[param]) in [int, float]:
                    result_copy[param] = marks * weightages[param]
                else:
                    raise Exception('Marks and weightages for a parameter should be a number or number list. Marks cannot be a single number and weightages a list for same parameter.')
            else:
                raise Exception('Marks for a parameter should be either a number or number list and not NaN')

        return Result(self.team_id, self.file, result_copy, self.pkg_path)

    def _aggregate_test_cases(self, result_of_test_cases, average):
        '''
            A test cased result will be a list and not a float/int value
        '''
        total = 0
        for value in result_of_test_cases:
            if type(value) == str and utils.is_string_number(value):
                total += utils.is_string_number(value)
            else:
                total += value
        if average:
            total = float(total / len(result_of_test_cases))
        return total

    @staticmethod
    def join(*results):
        '''
            Results should have same team_id but from different tests like either file should be different or package path
        '''
        if len(results) < 1:
            return None

        team_ids = set(map(lambda result: result.team_id, results))
        
        if len(team_ids) > 1:
            raise Exception('Results should have same team_ids')

        file_list = []
        pkg_path_list = []
        result_dict = {}
        comment = []

        for result in results:
            if type(result.file) == list:
                file_list += result.file
            else:
                file_list.append(result.file)

            if type(result.pkg_path) == list:
                pkg_path_list += result.pkg_path
            else:
                pkg_path_list.append(result.pkg_path)

            if type(result.comment) == list:
                comment += result.comment
            else:
                comment.append(result.comment)

            result_dict.update(result.result_dict)

        joined_result = Result(list(team_ids)[0], file_list, result_dict, pkg_path=pkg_path_list, comment=comment)
        return joined_result


class ResultGroup:
    '''
        Result group is an iterator. Try not to mutate it and expect it to work fabulously thereafter.
    '''
    def __init__(self, task_name: str, theme_name: str, results):
        self.task_name = task_name
        self.theme_name = theme_name
        if type(results) == list:
            self.dict_of_results = {result.team_id if type(result.team_id) == int else result.team_id: result for result in results}
        else:
            self.dict_of_results = results
        self._iter = iter(self.dict_of_results)

    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.dict_of_results)

    def __next__(self):
        try:
            self.curr_idx = next(self._iter)
            idx = self.curr_idx
            return self.dict_of_results[self.curr_idx]
        except StopIteration:
            self._iter = iter(self.dict_of_results)
            raise StopIteration

    def __eq__(self, value):
        if not isinstance(value, ResultGroup):
            return False
        if self.task_name != value.task_name:
            return False
        if self.theme_name != value.theme_name:
            return False
        if self.dict_of_results != value.dict_of_results:
            return False
        return True

    def __ne__(self, value):
        return not self.__eq__(value)

    def __repr__(self):
        return "ResultGroup(task_name: {}, theme_name: {}, dict_of_results: {})".format(self.task_name, self.theme_name, self.dict_of_results)

    def __str__(self):
        return self.__repr__()
        
    def __getitem__(self, team_id):
        try:
            if isinstance(team_id, slice):
                dict_of_results = {}
                for ii in range(*team_id.indices(team_id.stop)):
                    if self[ii] != None:
                        dict_of_results[ii] = self[ii]
                return ResultGroup(self.task_name, self.theme_name, dict_of_results)
            elif type(team_id) == str:
                if self.dict_of_results.get(team_id) != None:
                    return self.dict_of_results[team_id]
                elif self.dict_of_results.get(int(team_id)) != None:
                    return self.dict_of_results[int(team_id)]
            elif type(team_id) == int:
                if self.dict_of_results.get(team_id) != None:
                    return self.dict_of_results[team_id]
                elif self.dict_of_results.get(str(team_id)) != None:
                    return self.dict_of_results[str(team_id)]
        except KeyError:
            return None
    
    def find_by_id(self, id):
        # find result quickly by exploiting the fact that results are stored in sorted order
        for team_id, result in self.dict_of_results.items():
            if result.team_id == id:
                return result

    def to_dict(self):
        result_group = {}
        result_group['task_name'] = self.task_name
        result_group['theme_name'] = self.theme_name
        
        dict_of_results = {}
        for team_id, result in self.dict_of_results.items():
            dict_of_results[team_id] = result.to_dict()
        result_group['dict_of_results'] = dict_of_results
        return result_group

    @staticmethod
    def from_dict(group_dict):
        dict_of_results = {}
        for team_id, result in group_dict['dict_of_results'].items():
            dict_of_results[int(team_id)] = Result.from_dict(result)
        
        return ResultGroup(group_dict['task_name'], group_dict['theme_name'], dict_of_results)

    @staticmethod
    def result_group_file_name(self):
        return 'result_group_{}_{}'.format(self.theme_name, self.task_name)

    @staticmethod
    def from_json(file_path):
        # convert submissions array to json array
        if os.path.isdir(file_path):
            for file_name in os.listdir(file_path):
                if file_name.startswith('result_group_'):
                    json_file_path = os.path.join(file_path, file_name + '.json')
                    break
        else:
            json_file_path = file_path

        with open(json_file_path, 'r') as json_file:
            result_group_dict = json.load(json_file)
        
        return ResultGroup.from_dict(result_group_dict)

    def to_json(self, save_path):
        # convert submissions array to json array
        file_name = 'result_group_{}_{}'.format(self.theme_name, self.task_name)
        if os.path.isdir(save_path):
            json_file_path = os.path.join(save_path, file_name + '.json')
        else:
            json_file_path = save_path

        result_group_dict = self.to_dict()
        
        with open(json_file_path, 'w') as json_file:
            json.dump(result_group_dict, json_file)
        
    def to_csv(self, save_location):
        # comments regarding what are restrictions on theme name and task name
        file_name = 'result_group_{}_{}'.format(self.theme_name, self.task_name)
        file_path = os.path.join(save_location, file_name)

        try:
            # create csv
            list_of_dictionary = list(map(lambda result: result.get_dict(), self.dict_of_results))
            df = pd.DataFrame(list_of_dictionary)
            df.to_csv(file_path + '.csv', index=False)
            
            # create json
            meta_dict = {'task_name': self.task_name, 'theme_name': self.theme_name}
            with open(file_path + '.json', 'w+') as json_file:
                json.dump(meta_dict, json_file)

        except Exception as e:
            traceback.print_exc(e)
            return False
        return True

    @staticmethod
    def _find_result_group_files(save_location, theme_name, task_name):
        if theme_name == '' or theme_name == None:
            if task_name == '' or task_name == None:
                pattern = re.compile("result_group_.*_.*\.(csv|json)$")
            else:
                pattern = re.compile("result_group_.*_{}\.(csv|json)$".format(task_name))
        elif task_name == '' and task_name == None:
            pattern = re.compile("result_group_{}_.*\.(csv|json)$".format(theme_name))
        else:
            pattern = re.compile("result_group_{}_{}\.(csv|json)$".format(theme_name, task_name))

        csv_file_name = ''
        meta_file_name = ''

        list_of_items = os.listdir(save_location)
        for item in list_of_items:
            m = pattern.search(item)
            if m != None:
                file_extension = m.group(1)
                if file_extension == 'csv':
                    complement_file_name = os.path.splitext(item)[0] + '.json'
                    if complement_file_name in list_of_items:
                        meta_file_name = complement_file_name
                        csv_file_name = m.group(0)
                elif file_extension == 'json':
                    complement_file_name = os.path.splitext(item)[0] + '.csv'
                    if complement_file_name in list_of_items:
                        meta_file_name = m.group(0)
                        csv_file_name = complement_file_name
        
        csv_path = os.path.join(save_location, csv_file_name)
        meta_path = os.path.join(save_location, meta_file_name)

        return csv_path, meta_path

    @staticmethod
    def from_csv(save_location, theme_name='', task_name=''):
        # read csv into pandas dataframe
        # iterate and convert each row into a Result object
        # finally create a ResultGroup
        
        csv_path, meta_path = ResultGroup._find_result_group_files(save_location, theme_name, task_name)

        dict_of_results = []

        df = pd.read_csv(csv_path, index_col=None)
        for item in df.itertuples(index=False):
            info_dict = {}
            info_dict['team_id'] = item.team_id
            info_dict['file'] = item.file
            info_dict['pkg_path'] = item.pkg_path
            result_dict = utils.subtract_dict(dict(item._asdict()), info_dict)
            if info_dict['pkg_path'] == '' or info_dict['pkg_path'] == None:
                result = Result(info_dict['team_id'], info_dict['file'], result_dict)
            else:
                result = Result(info_dict['team_id'], info_dict['file'], result_dict, pkg_path=info_dict['pkg_path'])
            dict_of_results.append(result)

        # print(dict_of_results)
        # read json file
        with open(meta_path, 'r') as json_file:
            result_meta = json.load(json_file)
        
        # print(result_meta)
        return ResultGroup(result_meta['task_name'], result_meta['theme_name'], dict_of_results)

    def make_comments(self):
        dict_of_results = copy.deepcopy(self.dict_of_results)
        for team_id, result in self.dict_of_results.items():
            dict_of_results[team_id].comment = self._build_comment(result, *self._args, **self._kwargs)           
        return ResultGroup(self.task_name, self.theme_name, dict_of_results)

    def comment_builder(self, method, *args, **kwargs):
        self._build_comment = method
        self._args = args
        self._kwargs = kwargs
