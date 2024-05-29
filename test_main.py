import unittest
from unittest.mock import MagicMock
import main  

class TestMainScript(unittest.TestCase):
    def setUp(self):
        # Mocking the functions from other modules
        self.mock_csv_loader = MagicMock()
        self.mock_calculate = MagicMock()
        self.mock_visio = MagicMock()

    def test_load_data(self):
        # Mock the CSVLoader classes
        csv_loader_classes = {
            'CSVLoader1': self.mock_csv_loader,
            'CSVLoader2': self.mock_csv_loader,
            'CSVLoader3': self.mock_csv_loader
        }

        # Call the load_data function for each CSVLoader class
        for csv_loader_name, csv_loader_mock in csv_loader_classes.items():
            # Mock the process_data method
            csv_loader_mock_instance = MagicMock()
            csv_loader_mock.return_value = csv_loader_mock_instance
            csv_loader_mock_instance.process_data.return_value = None

            # Mock the load_dataframe method
            csv_loader_mock_instance.load_dataframe.return_value = "Mock DataFrame"

            # Call load_data
            result = main.load_data(
                csv_loader_class=csv_loader_mock,
                csv_filename="test.csv",
                table_name="test_table"
            )

            # Assertions
            self.assertEqual(result, "Mock DataFrame")
            csv_loader_mock.assert_called_once_with(main.database_file, "test_table")
            csv_loader_mock_instance.process_data.assert_called_once_with("test.csv")
            csv_loader_mock_instance.load_dataframe.assert_called_once_with("test.csv")

    def test_main(self):
        # Mock the functions and dataframes
        main.load_data = MagicMock(side_effect=[1, 2, 3])  # Mock the load_data function to return values
        main.calculate.calculate_least_square = MagicMock(return_value={'mock_result': 'mock_value'})
        main.calculate.generate_individual_tables = MagicMock(return_value={'mock_individual_tables': 'mock_value'})
        main.visio.ResultVisualizer = MagicMock()  # Mock the ResultVisualizer class

        # Call main function
        main.main()

        # Assertions
        main.load_data.assert_any_call(main.CSVLoader1, 'train.csv', 'train')
        main.load_data.assert_any_call(main.CSVLoader2, 'test.csv', 'test')
        main.load_data.assert_any_call(main.CSVLoader3, 'ideal.csv', 'ideal')
        main.calculate.calculate_least_square.assert_called_once_with(1, 3)
        main.calculate.generate_individual_tables.assert_called_once_with(3, 2, {'mock_result': 'mock_value'})
        main.visio.ResultVisualizer.assert_called()  # Assert that the ResultVisualizer class was instantiated

if __name__ == '__main__':
    unittest.main()
