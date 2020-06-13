class TestUtils:
    @staticmethod
    def equivalent_solutions(result, expected):
        for case in result:
            equivalent_to_an_expected_case = False
            for expected_case in expected:
                if case.is_equivalent_to(expected_case):
                    equivalent_to_an_expected_case = True
            if not equivalent_to_an_expected_case:
                return False
        return True
