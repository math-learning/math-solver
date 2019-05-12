import unittest
from src.utils.list.index_combinations_strategy_only_continuous import OnlyContinuousIndexCombinationStrategy


class TestIndexCombinationsStrategyOnlyContinuous(unittest.TestCase):

    def test_get_combinations(self):
        strategy = OnlyContinuousIndexCombinationStrategy()
        combinations = strategy.combinations_of_n_elements(["a","b","c"], 2)
        print("hello")