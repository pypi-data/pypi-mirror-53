import os
import csv
import sys
import glob
import traceback
import multiprocessing as mp

from gradefast import utils
from gradefast.aggregate import Aggregate
from gradefast.result import Result, ResultGroup
from gradefast.test import GFCliTest, GFTest, TestType
from gradefast.submission import Submission, SubmissionGroup

class Evaluate:
    def __init__(self, submissions, test, result_path='./', clean=True):
        # Submissions contain multiple test entry points for example main.py, result.txt, result.png 
        # Multiple tests per Submission takes care of evaluating these multiple files
        # Result from each of these tests may or may not be aggregated
        # Alternatively, there can be a single test evaluating all of these files 
        # evaluate tests on each submission
        self.submissions = submissions
        self.test = test
        self.result_path = result_path
        # len of tests should be same as marking_scheme
        self.clean = True
        

    def _pkg_setup_wrapper(self, submission, test, conn):
        # get submission's unzipped file path
        result_dict = {}
        comment = ''
        exception_tr = []
        try:
            full_pkg_path = self._make_pkg_full_path(submission, test)
            print(full_pkg_path)
            full_pkg_path = glob.glob(full_pkg_path)[0]
            print(full_pkg_path)
            sys.path.append(full_pkg_path)

            result_dict, comment, exception_tr = test(submission)
            if result_dict == None:
                result_dict = {}
            if comment == None:
                comment = ''
            if exception_tr == None:
                exception_tr = []

            conn.send([result_dict, comment, exception_tr])
            conn.close()
        except Exception as e:
            exception = traceback.format_exc()
            print(exception)
            conn.send([{}, '', [exception]])
            conn.close()

    # TODO(manjrekarom): Handle unzipping of zips
    def _make_pkg_full_path(self, submission, test):
        # check file_to_test starts with zip[number] or unzipped[number]
        # find the [number]
        # pickup path of the file/ directory from submission.file_paths
        # optionally unzip if no zip is present
        # check package_path
        # match (case insensitively) if there is a path in the submission folder like that
        # ignore team_id matches
        # return the path
        file_to_test = test.file_to_test

        parition_name = ''
        if file_to_test.startswith('zip'):
            # a proper file name will consist of <team_id>_<extension><number>
            parition_name = file_to_test.split('zip')
        elif file_to_test.startswith('unzipped'):
            parition_name = file_to_test.split('unzipped')

        unzipped_pkg_path = ''
        if len(parition_name) > 2:
            raise Exception('The file to test parameter is incorrect. It should be an extension type followed by an integer')
        else:
            if parition_name[0] == '':
                if utils.is_string_number(parition_name[1]) or parition_name[1] == '':
                    unzipped_pkg_path = submission.items[file_to_test]['path']
                else:
                    raise Exception('File to test should be followed by a number if at all')
            else:
                raise Exception('File to test specified doesnt look right')
        return os.path.abspath(os.path.join(unzipped_pkg_path, test.package_path))

    def _evaluate(self, submission, test, mark=None):
        '''
            Returns result_dict, comment and exceptions
        '''
        try:
            if isinstance(test, GFCliTest):
                result_dict = test(submission)
            elif isinstance(test, GFTest):
                if test.test_type == TestType.FILE:
                    # provide file path as a parameter to the test function
                    # take the returned result
                    # transform it into marks
                    # save the result into some file
                    file_path = submission.file_paths[test.file_to_test]
                    result_dict = test(file_path)
                elif test.test_type == TestType.PKG:
                    # Only for python submisions right now
                    # mount the student package
                    # run test function
                    # take the returned result
                    # transform it into marks
                    # save the result to some file

                    # import package
                    # TODO: package_path may be a list of packages

                    # get context and create a process
                    ctx = mp.get_context()
                    par_conn, child_conn = ctx.Pipe()
                    p = ctx.Process(target=self._pkg_setup_wrapper, args=(submission, test, child_conn,))
                    p.start()
                    result_dict, comment, exception_tr = par_conn.recv()
                    p.join()
        except Exception as e:
            # log all exceptions
            print(traceback.format_exc())

        return result_dict, comment, exception_tr

    # TODO return result group
    def __call__(self):
        # evaluate
        # on each submission in submissions run each test in tests
        task_name = ''
        theme_name = ''

        if isinstance(self.submissions, SubmissionGroup):
            task_name = self.submissions.task_name
            theme_name = self.submissions.theme_name

        result_group = ResultGroup(task_name, theme_name, {})
        exceptions = []

        for idx, submission in enumerate(self.submissions):
            # print(submission.file_list)
            # evaluate
            # if marks are not given, do no transformation of result
            
            result_dict, comment, exception = self._evaluate(submission, self.test)
            print('TEAM ID: {} {}'.format(submission.team_id, result_dict))
            result = Result(submission.team_id, self.test.file_to_test, result_dict, pkg_path=self.test.package_path, comment=comment)
            result_group = Aggregate.combine(ResultGroup(task_name, theme_name, {result.team_id: result}), result_group)
            result_group.to_json(self.result_path)
            exceptions.append(exception)

        return result_group, exceptions
