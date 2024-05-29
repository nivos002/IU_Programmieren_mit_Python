import unittest
import pandas as pd
from unittest.mock import patch
from visio import ResultVisualizer

class TestResultVisualizer(unittest.TestCase):
    def setUp(self):
        # Create sample dataframes for testing
        self.df_ideal = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [2, 3, 4, 5],
            'y2': [3, 4, 5, 6]
        })
        
        self.best_fit_result = {
            'y1': {'best_fit_col_ideal': 'y1'},
            'y2': {'best_fit_col_ideal': 'y2'}
        }
        
        self.df_train = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 2, 3, 4],
            'y2': [2, 3, 4, 5]
        })

        self.individual_tables = {
            'y1': pd.DataFrame({
                'x': [1, 2, 3, 4],
                'ideal_y': [2, 3, 4, 5],
                'test_y': [1.5, 3.5, 4.5, 6.5],
                'distance': [0.5, 0.5, 0.5, 0.5],
                'result': [True, True, True, True],
                'ideal_function_number': ['1', '1', '1', '1']
            }),
            'y2': pd.DataFrame({
                'x': [1, 2, 3, 4],
                'ideal_y': [3, 4, 5, 6],
                'test_y': [1.5, 3.5, 4.5, 6.5],
                'distance': [1.5, 0.5, 0.5, 0.5],
                'result': [False, True, True, True],
                'ideal_function_number': ['2', '2', '2', '2']
            })
        }

    @patch('matplotlib.pyplot.show')
    def test_plot_results_1(self, mock_show):
        visualizer = ResultVisualizer()
        visualizer.plot_results_1(self.df_ideal, self.best_fit_result, self.df_train)
        mock_show.assert_called()

    @patch('matplotlib.pyplot.show')
    def test_plot_result_2(self, mock_show):
        visualizer = ResultVisualizer()
        visualizer.plot_result_2(self.individual_tables, self.best_fit_result)
        mock_show.assert_called()

if __name__ == '__main__':
    unittest.main()
