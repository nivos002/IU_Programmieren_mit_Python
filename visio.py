import matplotlib.pyplot as plt
import pandas as pd

class ResultVisualizer:
    """
    A class for visualizing results of data analysis.

    Methods:
        plot_results_1: Plot the comparison between training data and ideal functions.
        plot result_2: Plot the comparison between the ideal function and the test data.
    """
    def __init__(self):
        pass

    def plot_results_1(self, df_ideal, best_fit_result, df_train):
        """
        Plot the comparison between training data and ideal functions.

        Parameters:
            df_ideal (pd.DataFrame): Ideal dataset with 'x' as the first column and Y columns thereafter.
            best_fit_result (dict): Dictionary containing the best fit in the ideal dataset for each Y-column in the training dataset.
            df_train (pd.DataFrame): Training dataset with 'x' as the first column and Y columns thereafter.
        """
        try:
            from main import CustomError  # Import CustomError from main.py
            
            # Check if the input dataframes are of the correct type
            if not isinstance(df_ideal, pd.DataFrame) or not isinstance(df_train, pd.DataFrame):
                raise CustomError("DataFrames df_ideal and df_train must be of type pd.DataFrame")
                
            # Check if the 'x' column is present in the dataframes
            if 'x' not in df_ideal.columns or 'x' not in df_train.columns:
                raise CustomError("DataFrames must contain column 'x'")

            # Get the list of Y-columns in the training dataset
            y_columns = df_train.columns[1:]

            for idx, col_train in enumerate(y_columns):
                col_ideal = best_fit_result[col_train]['best_fit_col_ideal']

                # Plot the Ideal function as a line
                plt.figure(figsize=(10, 6))
                plt.plot(df_ideal['x'], df_ideal[col_ideal], label=f'Ideal function ({col_ideal})', color='green')

                # Plot the Train data as points
                plt.scatter(df_train['x'], df_train[col_train], label=f'Training data ({col_train})', marker='o', s=10, color='orange')

                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('Comparison between Training Data and Ideal Functions')
                plt.legend()
                plt.grid(True)
                
                # Show the plot for the current Y-column
                plt.show()

        except CustomError as e:
            print("Custom Error:", e.message)
            # Perform alternative actions or exit the program

        except (TypeError, KeyError, IndexError) as e:
            print("Standard Error:", e)
            # Perform alternative actions or exit the program

        except Exception as e:
            print("Unexpected Error:", e)
            # Perform alternative actions or exit the program

    def plot_result_2(self, individual_tables, best_fit_result):
        """
        Visualize individual tables as plots.

        Parameters:
            individual_tables (dict): Dictionary containing individual tables for each Y-column in the ideal dataset.
            best_fit_result (dict): Dictionary containing the best fit in the ideal dataset for each Y-column in the training dataset.
        """
        try:
            from main import CustomError  # Import CustomError from main.py
            
            # Check if the input data structures are dictionaries
            if not isinstance(individual_tables, dict) or not isinstance(best_fit_result, dict):
                raise CustomError("Input parameters must be dictionaries")

            for column, table in individual_tables.items():
                ideal_y = table['ideal_y']
                test_y = table['test_y']
                true_indices = table[table['result'] == True].index
                ideal_function_name = f"Ideal function ({best_fit_result[column]['best_fit_col_ideal']})"
                
                plt.figure(figsize=(10, 6))
                plt.plot(table['x'], ideal_y, label=f'{ideal_function_name}', color='green')
                plt.scatter(table['x'], test_y, color='orange', label='Test Data')
                plt.scatter(table.loc[true_indices, 'x'], table.loc[true_indices, 'test_y'], color='red', label='True Points')
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title(f'Comparison between {ideal_function_name} and Test Data')
                plt.legend()
                plt.grid(True)
              
            # Show all plots
            plt.tight_layout()
            plt.show()

        except CustomError as e:
            print("Custom Error:", e.message)
            # Perform alternative actions or exit the program

        except (TypeError, KeyError, IndexError) as e:
            print("Standard Error:", e)
            # Perform alternative actions or exit the program

        except Exception as e:
            print("Unexpected Error:", e)
            # Perform alternative actions or exit the program



            









