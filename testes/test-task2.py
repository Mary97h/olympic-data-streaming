import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import unittest
from operators import (
    data_join_operator, duplicate_check_operator,
    data_grouping_by_nationality_operator, average_score_calculation_operator,
    highest_score_retrieval_operator, display_average_and_top_player_operator,
    overall_best_group_and_top_three_operator
)

class TestTask2Pipeline(unittest.TestCase):
    def setUp(self):
        # Sample data from the assessment
        names = ["Alex", "Peter", "Josef", "Max", "Peter"]
        scores = [7, 2, 8, 4, 2]
        nationalities = ["Austria", "US", "US", "Austria", "US"]
        
        # Operator 1: Join data
        joined_data = data_join_operator(names, scores, nationalities)
        
        # Operator 2: Check duplicates
        self.deduplicated_data = duplicate_check_operator(joined_data)
    
    def test_data_grouping_by_nationality(self):
        # Operator 3: Group by nationality
        grouped_data = data_grouping_by_nationality_operator(self.deduplicated_data)
        
        # Verify structure and content
        self.assertEqual(len(grouped_data), 2)  # Austria and US
        self.assertEqual(len(grouped_data["Austria"]), 2)
        self.assertEqual(len(grouped_data["US"]), 2)
        
        # Check specific records are in correct groups
        austria_names = [record["name"] for record in grouped_data["Austria"]]
        us_names = [record["name"] for record in grouped_data["US"]]
        
        self.assertIn("Alex", austria_names)
        self.assertIn("Max", austria_names)
        self.assertIn("Peter", us_names)
        self.assertIn("Josef", us_names)
    
    def test_average_score_calculation(self):
        # Set up
        grouped_data = data_grouping_by_nationality_operator(self.deduplicated_data)
        
        # Operator 4: Calculate average scores
        avg_scores = average_score_calculation_operator(grouped_data)
        
        # Verify results match expected output
        self.assertAlmostEqual(avg_scores["Austria"], 5.5)
        self.assertAlmostEqual(avg_scores["US"], 5.0)
    
    def test_highest_score_retrieval(self):
        # Set up
        grouped_data = data_grouping_by_nationality_operator(self.deduplicated_data)
        
        # Operator 5: Get highest score for each group
        top_players = highest_score_retrieval_operator(grouped_data)
        
        # Verify best players
        self.assertEqual(top_players["Austria"]["name"], "Alex")
        self.assertEqual(top_players["Austria"]["score"], 7)
        self.assertEqual(top_players["US"]["name"], "Josef")
        self.assertEqual(top_players["US"]["score"], 8)
    
    def test_display_average_and_top_player(self):
        # Set up
        grouped_data = data_grouping_by_nationality_operator(self.deduplicated_data)
        avg_scores = average_score_calculation_operator(grouped_data)
        top_players = highest_score_retrieval_operator(grouped_data)
        
        # Operator 6: Format the result for display
        result = display_average_and_top_player_operator(avg_scores, top_players)
        
        # Convert to dictionary for easier testing
        result_dict = {r["nationality"]: r for r in result}
        
        # Verify the results match expected
        self.assertAlmostEqual(result_dict["Austria"]["average_score"], 5.5)
        self.assertEqual(result_dict["Austria"]["top_player"], "Alex (7)")
        self.assertAlmostEqual(result_dict["US"]["average_score"], 5.0)
        self.assertEqual(result_dict["US"]["top_player"], "Josef (8)")
    
    def test_overall_best_group_and_top_three(self):
        # Set up
        grouped_data = data_grouping_by_nationality_operator(self.deduplicated_data)
        avg_scores = average_score_calculation_operator(grouped_data)
        
        # Operator 7: Overall stats
        result = overall_best_group_and_top_three_operator(grouped_data, avg_scores)
        
        # Verify best group
        self.assertEqual(result["best_group"]["nationality"], "Austria")
        self.assertAlmostEqual(result["best_group"]["average_score"], 5.5)
        
        # Verify top three individuals
        top_three = result["top_three_individuals"]
        self.assertEqual(len(top_three), 3)
        self.assertEqual(top_three[0], "Josef (8)")
        self.assertEqual(top_three[1], "Alex (7)")
        self.assertEqual(top_three[2], "Max (4)")

if __name__ == "__main__":
    unittest.main(verbosity=2)