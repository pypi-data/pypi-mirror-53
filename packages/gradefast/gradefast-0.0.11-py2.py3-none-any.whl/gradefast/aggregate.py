from gradefast.result import Result, ResultGroup

class Aggregate:
    @staticmethod
    def combine(*result_groups):
        '''
            Combines records/rows from multiple result_groups
            Assumes result_groups are of same type
        ''' 
        final_dict = {}
        for group in result_groups:
            final_dict.update(group.dict_of_results)
        if len(result_groups) > 0: 
            combined_group = ResultGroup(result_groups[0].task_name, result_groups[0].theme_name, final_dict)
            return combined_group
        return None

    @staticmethod
    def add(*result_groups):
        '''
            Add all parameters to form a final total
        '''
        return Aggregate.operate('add', *result_groups)

    @staticmethod
    def multiply(weightages, *result_groups):
        '''
            Add all parameters to form a final total
        '''
        return Aggregate.operate('multiply', *result_groups, weightages=weightages)

    @staticmethod
    def flatten_test_cases(*result_groups):
        '''
            Add all parameters to form a final total
        '''
        return Aggregate.operate('flatten_test_cases', *result_groups)

    @staticmethod
    def operate(method, *result_groups, weightages={}):
        if len(result_groups) > 0:
            combined_group = Aggregate.combine(*result_groups)
            final_result = {}
            for result in combined_group:
                if method == 'flatten_test_cases':
                    final_result[result.team_id] = result.flat_result()
                elif method == 'multiply':
                    final_result[result.team_id] = result.multiply(weightages)
                elif method == 'add':
                    final_result[result.team_id] = result.add()
            combined_group.dict_of_results = final_result
            return combined_group

    @staticmethod
    def join(*result_groups):
        '''
            Stack columns from multiple results
        '''
        task_names = set(map(lambda group: group.task_name, result_groups))
        if len(task_names) > 1:
            raise Exception('Result groups you are joining should be for the same task')

        theme_names = set(map(lambda group: group.theme_name, result_groups))
        if len(theme_names) > 1:
            raise Exception('Result groups you are joining should be for the same theme')

        # select results with particular team_ids and run join method on them
        team_ids = set()
        for group in result_groups:
            team_ids = team_ids.union(set(map(lambda team_id: team_id, group.dict_of_results)))
            
        final_results_dict = {}
        for team_id in team_ids:
            joined_result = {}
            for group in result_groups:
                if joined_result == {}:
                    joined_result = Result.join(group[team_id])
                else:
                    joined_result = Result.join(group[team_id], joined_result)
            final_results_dict[team_id] = joined_result
        
        return ResultGroup(result_groups[0].task_name, result_groups[0].theme_name, final_results_dict)
