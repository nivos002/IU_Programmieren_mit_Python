import pandas as pd
import numpy as np
from csvloader import CSVLoader1, CSVLoader2, CSVLoader3
import calculate
import visio

# Custom Exception Class
class CustomError(Exception):
    """
    Custom exception class for handling specific errors in the program.

    Attributes:
        message (str): A descriptive message explaining the error.
    """
    def __init__(self, message):
        """
        Initializes the CustomError object with the given message.

        Parameters:
            message (str): A descriptive message explaining the error.
        """
        self.message = message

def main():
    """
    Main function to demonstrate the usage of loading data from CSV, performing calculations,
    and visualizing results.
    """
    try:
        database_file = 'Test-DB.db'

        # Function to load data from CSV into DataFrame
        def load_data(csv_loader_class, csv_filename, table_name):
            """
            Load data from CSV file into DataFrame using the specified CSV loader class.

            Parameters:
                csv_loader_class (class): The CSV loader class to use for loading data.
                csv_filename (str): The name of the CSV file to load.
                table_name (str): The name of the table corresponding to the CSV data.

            Returns:
                pd.DataFrame: The loaded DataFrame.
            """
            csv_loader = csv_loader_class(database_file, table_name)
            csv_loader.process_data(csv_filename)
            return csv_loader.load_dataframe(csv_filename)

        # Load data from CSV files
        df_train = load_data(CSVLoader1, 'train.csv', 'train')
        df_test = load_data(CSVLoader2, 'test.csv', 'test')
        df_ideal = load_data(CSVLoader3, 'ideal.csv', 'ideal')

        # Perform calculations using the calculate module
        best_fits = calculate.calculate_least_square(df_train, df_ideal)

        # Display the best fit Y-column 
        for col_train, result in best_fits.items():
            print(f"\nBest fit for Y-column '{col_train}' in Train DataFrame:")
            print(f"Best fit Y-column in Ideal DataFrame: '{result['best_fit_col_ideal']}', Squared Difference = {result['squared_diff']}\n")

        # Call the function after calculating the best fits in your `main` function
        individual_tables = calculate.generate_individual_tables(df_ideal, df_test, best_fits)
            
        # Create an instance of the ResultVisualizer class
        visualizer = visio.ResultVisualizer()

        # Call the method to plot the results and pass the result_tables
        visualizer.plot_results_1(df_ideal, best_fits, df_train)

        visualizer.plot_result_2(individual_tables, best_fits)

    except CustomError as e:
        print("Custom Error:", e.message)
        # Perform alternative actions or exit the program

    except (TypeError, KeyError, IndexError) as e:
        print("Standard Error:", e)
        # Perform alternative actions or exit the program

    except Exception as e:
        print("Unexpected Error:", e)
        # Perform alternative actions or exit the program

if __name__ == "__main__":
    main()

