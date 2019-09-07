from mathlearning.mappers.theorem_mapper import TheoremMapper
from mathlearning.utils.logger import Logger
from mathlearning.model.exercise import Exercise
from mathlearning.model.expression import Expression


class ValidateMapperException(Exception):
    pass


class ValidateMapper:
    def __init__(self):
        self.theoremMapper = TheoremMapper()
        self.logger = Logger.getLogger()
    
    def parse_validate_new_step_input(self, request_data):
        self.logger.info("Parsing validate new step request data: {}".format(request_data))
        try:
            theorems = request_data['theorems']
            new_expression = request_data['new_expression']
            old_expression = request_data['old_expression']
            
            #TODO: Do a better handling of this case
            if new_expression == old_expression:
                raise Exception()

            new_expr = Expression(new_expression)
            old_expr = Expression(old_expression)

            parsed_theorems = self.theoremMapper.from_json_to_theorems(theorems)

            return new_expr, old_expr, parsed_theorems
        except Exception as e:
            self.logger.error("Error while parsing validate new step input: {}".format(e))
            raise ValidateMapperException(e)

    def parse_validate_result_input(self, request_data):
        self.logger.info("Parsing validate result request data: {}".format(request_data))
        try:
            exercise_dto = request_data['exercise']
            theorems_dto = exercise_dto['theorems']

            theorems = self.theoremMapper.from_json_to_theorems(theorems_dto)
            result = Expression(exercise_dto['result'])
            input_data = Expression(exercise_dto['input_data'])

            exercise = Exercise(input_data, theorems, result)

            steps_dto = request_data['steps']
            steps = []
            for step_dto in steps_dto:
                steps.append(Expression(step_dto))

            return steps, exercise
        except Exception as e:
            self.logger.error("Error while parsing validate result input: {}".format(e))
            raise ValidateMapperException(e)

    def  parse_compare_expressions_data(self, request_data):
        self.logger.info("Parsing validate not in history request data: {}".format(request_data))
        try:
            expression_one_str = request_data['expression_one']
            expression_two_str = request_data['expression_two']

            expression_one = Expression(expression_one_str)
            expression_two = Expression(expression_two_str)
            
            return (expression_one, expression_two)

        except Exception as e:
            self.logger.error("Error while parsing validate result input: {}".format(e))
            raise ValidateMapperException(e)


    def parse_validate_not_in_history_input(self, request_data):
        self.logger.info("Parsing validate not in history request data: {}".format(request_data))
        try:
            new_expression = request_data['new_expression']
            history_dto = request_data['history']

            history = []
            for history_item in history_dto:
                history.append(history_item)
    
            return new_expression, history
        except Exception as e:
            self.logger.error("Error while parsing validate result input: {}".format(e))
            raise ValidateMapperException(e)