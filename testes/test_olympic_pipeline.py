import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
from operators import data_join_operator, duplicate_check_operator

class TestOlympicPipeline(unittest.TestCase):

    def test_data_join_operator(self):
        names = ["Alex", "Peter", "Josef", "Max", "Peter"]
        scores = [7, 2, 8, 4, 2]
        nationalities = ["Austria", "US", "US", "Austria", "US"]

        result = data_join_operator(names, scores, nationalities)
        
        expected = [
            {"name": "Alex", "score": 7, "nationality": "Austria"},
            {"name": "Peter", "score": 2, "nationality": "US"},
            {"name": "Josef", "score": 8, "nationality": "US"},
            {"name": "Max", "score": 4, "nationality": "Austria"},
            {"name": "Peter", "score": 2, "nationality": "US"},
        ]

        self.assertEqual(result, expected)

    def test_duplicate_check_operator(self):
        records = [
            {"name": "Alex", "score": 7, "nationality": "Austria"},
            {"name": "Peter", "score": 2, "nationality": "US"},
            {"name": "Josef", "score": 8, "nationality": "US"},
            {"name": "Max", "score": 4, "nationality": "Austria"},
            {"name": "Peter", "score": 2, "nationality": "US"},
        ]

        result = duplicate_check_operator(records)

        expected = [
            {"name": "Alex", "score": 7, "nationality": "Austria"},
            {"name": "Peter", "score": 2, "nationality": "US"},
            {"name": "Josef", "score": 8, "nationality": "US"},
            {"name": "Max", "score": 4, "nationality": "Austria"},
        ]

        self.assertEqual(result, expected)
