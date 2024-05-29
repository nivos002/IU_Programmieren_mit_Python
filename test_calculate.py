import unittest
import pandas as pd
import numpy as np

def calculate_least_square(df_train, df_ideal):
    """
    Calculate the best fit and squared differences for each Y-column in the training dataset.

    Parameters:
        df_train (pd.DataFrame): Training dataset with 'x' as the first column and Y columns thereafter.
        df_ideal (pd.DataFrame): Ideal dataset with 'x' as the first column and Y columns thereafter.

    Returns:
        dict: A dictionary containing the best fit in the ideal dataset and the associated squared difference
              for each Y-column in the training dataset.
    """
    best_fits = {}

    # Loop through each column in the training dataset
    for col_train in df_train.columns[1:]:
        min_squared_diff = float('inf')
        best_fit_col_ideal = None

        # Loop through each column in the ideal dataset
        for col_ideal in df_ideal.columns[1:]:
            # Calculate squared differences between corresponding columns
            squared_diff_sum = sum((df_ideal[col_ideal] - df_train[col_train]) ** 2)

            # Update if current fit is better than previous best fit
            if squared_diff_sum < min_squared_diff:
                min_squared_diff = squared_diff_sum
                best_fit_col_ideal = col_ideal

        # Store the best fit and associated squared difference
        best_fits[col_train] = {'best_fit_col_ideal': best_fit_col_ideal, 'squared_diff': min_squared_diff, 'test_column': col_train}

    return best_fits

def generate_individual_tables(df_ideal, df_test, best_fits, output_dir='./'):
    """
    Generate individual tables for each Y-column in the ideal dataset and save them as CSV files.

    Parameters:
        df_ideal (pd.DataFrame): Ideal dataset with 'x' as the first column and Y columns thereafter.
        df_test (pd.DataFrame): Test dataset with 'x' as the first column and Y columns thereafter.
        best_fits (dict): Dictionary containing the best fit in the ideal dataset and the associated squared difference
                          for each Y-column in the training dataset.

    Returns:
        dict: A dictionary containing individual tables for each Y-column in the ideal dataset.
    """
    individual_tables = {}

    # Loop through each Y-column in the best fits dictionary
    for column, fit_info in best_fits.items():
        ideal_column = fit_info['best_fit_col_ideal']
        
        # Sort the test dataset in ascending order by the X column
        df_test_sorted = df_test.sort_values(by='x', ascending=True).reset_index(drop=True)
        
        # Adjust Y-values for both test and ideal functions
        adjusted_ideal_y = df_ideal.set_index('x').loc[df_test_sorted['x'], ideal_column].reset_index(drop=True)
        adjusted_test_y = df_test_sorted['y'].reset_index(drop=True)
        
        # Calculate distances between corresponding points in ideal and adjusted test datasets
        distances = np.abs(adjusted_ideal_y - adjusted_test_y)
        
        # Check if distance is less than square root of 2
        results = distances < np.sqrt(2)
        
        # Create individual table for the Y-column
        table_data = {
            'x': df_test_sorted['x'],
            'ideal_y': adjusted_ideal_y,
            'test_y': adjusted_test_y,
            'distance': distances,
            'result': results,
            'ideal_function_number': ideal_column.split('_')[-1]
        }
        
        individual_tables[column] = pd.DataFrame(table_data)
        
        # Include the Y-value of the ideal function in the table header
        print(f"Table for Ideal Y-column '{ideal_column}'")
        print(individual_tables[column])
        print("\n")

         # Save table with True values to CSV
        true_table = individual_tables[column][individual_tables[column]['result'] == True]
        true_table.to_csv(f"{output_dir}/True_Points_{ideal_column}.csv", index=False)
        print(f"True points for Ideal Y-column '{ideal_column}'")
        true_table = individual_tables[column][individual_tables[column]['result'] == True]
        print(true_table)
        print("\n")

    return individual_tables

class TestLeastSquare(unittest.TestCase):
    def setUp(self):
        # Create sample dataframes for testing
        self.df_train = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 2, 3, 4],
            'y2': [2, 3, 4, 5]
        })
        
        self.df_ideal = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [2, 3, 4, 5],
            'y2': [3, 4, 5, 6]
        })

    def test_calculate_least_square(self):
        best_fits = calculate_least_square(self.df_train, self.df_ideal)
        expected_result = {
            'y1': {'best_fit_col_ideal': 'y1', 'squared_diff': 0, 'test_column': 'y1'},
            'y2': {'best_fit_col_ideal': 'y2', 'squared_diff': 0, 'test_column': 'y2'}
        }
        self.assertDictEqual(best_fits, expected_result)

class TestGenerateIndividualTables(unittest.TestCase):
    def setUp(self):
        # Create sample dataframes for testing
        self.df_ideal = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [2, 3, 4, 5],
            'y2': [3, 4, 5, 6]
        })
        
        self.df_test = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y': [1.5, 3.5, 4.5, 6.5]
        })
        
        self.best_fits = {
            'y1': {'best_fit_col_ideal': 'y1', 'squared_diff': 0, 'test_column': 'y1'},
            'y2': {'best_fit_col_ideal': 'y2', 'squared_diff': 0, 'test_column': 'y2'}
        }

    def test_generate_individual_tables(self):
        individual_tables = generate_individual_tables(self.df_ideal, self.df_test, self.best_fits)
        expected_result = {
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
        for key in expected_result.keys():
            pd.testing.assert_frame_equal(individual_tables[key], expected_result[key])

if __name__ == '__main__':
    unittest.main()
