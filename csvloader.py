import csv
from sqlalchemy import create_engine, Table, Column, Float, MetaData, select
import pandas as pd

class BaseCSVLoader:
    """
    Base class for loading data from CSV files into a SQLite database.

    Attributes:
        database_file (str): The file path to the SQLite database.
        table_name (str): The name of the table to load the data into.
        engine: The database engine for connecting to the SQLite database.
        conn: The database connection.
        metadata: Metadata for the database.

    Methods:
        create_table: Method for creating the database table. Must be implemented in subclasses.
        process_data: Method for processing and loading data from a CSV file into the database table.
        extract_values: Method for extracting values from a row of the CSV file.
        load_dataframe: Method for loading the CSV data into a Pandas DataFrame.
    """
    def __init__(self, database_file, table_name):
        """
        Initializes the BaseCSVLoader class.

        Parameters:
            database_file (str): The file path to the SQLite database.
            table_name (str): The name of the table to load the data into.
        """
        self.database_file = database_file
        self.table_name = table_name

        # Establish a connection to the SQLite database
        self.engine = create_engine(f'sqlite:///{self.database_file}')
        self.conn = self.engine.connect()

        # Create metadata
        self.metadata = MetaData(bind=self.engine)

        # Define the table
        self.create_table()

        # Create the table in the database if it doesn't exist
        if not self.engine.dialect.has_table(self.engine, self.table_name):
            self.metadata.create_all()
            print(f"The '{self.table_name}' table has been created.")

    def create_table(self):
        """
        Abstract method for creating the database table.
        Must be implemented in subclasses.
        """
        pass

    def process_data(self, csv_file):
        """
        Processes and loads data from a CSV file into the database table.

        Parameters:
            csv_file (str): The file path to the CSV file.
        """
        pass

    def extract_values(self):
        """
        Abstract method for extracting values from a row of the CSV file.
        Must be implemented in subclasses.
        """
        pass

    def load_dataframe(self, csv_filename):
        """
        Loads the CSV data into a Pandas DataFrame.

        Parameters:
            csv_filename (str): The file path to the CSV file.

        Returns:
            pd.DataFrame: The loaded Pandas DataFrame.
        """
        return pd.read_csv(csv_filename)

class CSVLoader1(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with five columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with five columns (x, y1, y2, y3, y4).
        """
        pass

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        pass

class CSVLoader2(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with two columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with two columns (x, y1).
        """
        pass

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        pass

class CSVLoader3(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with 51 columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with 51 columns (x, y1, y2, ..., y50).
        """
        pass

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        pass
class BaseCSVLoader:
    """
    Base class for loading data from CSV files into a SQLite database.

    Attributes:
        database_file (str): The file path to the SQLite database.
        table_name (str): The name of the table to load the data into.
        engine: The database engine for connecting to the SQLite database.
        conn: The database connection.
        metadata: Metadata for the database.

    Methods:
        create_table: Method for creating the database table. Must be implemented in subclasses.
        process_data: Method for processing and loading data from a CSV file into the database table.
        extract_values: Method for extracting values from a row of the CSV file.
        load_dataframe: Method for loading the CSV data into a Pandas DataFrame.
    """
    def __init__(self, database_file, table_name):
        """
        Initializes the BaseCSVLoader class.

        Parameters:
            database_file (str): The file path to the SQLite database.
            table_name (str): The name of the table to load the data into.
        """
        self.database_file = database_file
        self.table_name = table_name

        # Establish a connection to the SQLite database
        self.engine = create_engine(f'sqlite:///{self.database_file}')
        self.conn = self.engine.connect()

        # Create metadata
        self.metadata = MetaData(bind=self.engine)

        # Define the table
        self.create_table()

        # Create the table in the database if it doesn't exist
        if not self.engine.dialect.has_table(self.engine, self.table_name):
            self.metadata.create_all()
            print(f"The '{self.table_name}' table has been created.")

    def create_table(self):
        """
        Abstract method for creating the database table.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("create_table method must be implemented in subclasses")

    def process_data(self, csv_file):
        """
        Processes and loads data from a CSV file into the database table.

        Parameters:
            csv_file (str): The file path to the CSV file.

        Raises:
            ValueError: If the CSV file is empty.
        """
        # Check if the table already contains data
        query = select([self.data_table])
        result = self.conn.execute(query)
        data = result.fetchall()
        data_count = len(data)
        if data_count > 0:
            print(f"\nThe '{self.table_name}' table already exists and contains data.")
            return

        # Read data from the CSV file and insert into the table
        with open(csv_file, 'r') as file:
            csv_data = csv.reader(file)
            header = next(csv_data, None)
            if header is None:
                raise ValueError("CSV file is empty")
            for row in csv_data:
                values = self.extract_values(row)
                self.conn.execute(self.data_table.insert().values(**values))
            print(f"Data has been successfully loaded from the CSV file into the '{self.table_name}' table.")

        # Close the database connection
        self.conn.close()

    def extract_values(self):
        """
        Abstract method for extracting values from a row of the CSV file.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("extract_values method must be implemented in subclasses")

    def load_dataframe(self, csv_filename):
        """
        Loads the CSV data into a Pandas DataFrame.

        Parameters:
            csv_filename (str): The file path to the CSV file.

        Returns:
            pd.DataFrame: The loaded Pandas DataFrame.
        """
        return pd.read_csv(csv_filename)

class CSVLoader1(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with five columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with five columns (x, y1, y2, y3, y4).
        """
        columns = [Column('x', Float), Column('y1', Float), Column('y2', Float), Column('y3', Float), Column('y4', Float)]
        self.data_table = Table(self.table_name, self.metadata, *columns)

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        if len(row) != 5:
            raise ValueError("Incorrect number of columns in CSV row")
        return {
            'x': float(row[0]),
            'y1': float(row[1]),
            'y2': float(row[2]),
            'y3': float(row[3]),
            'y4': float(row[4])
        }

class CSVLoader2(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with two columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with two columns (x, y1).
        """
        columns = [Column('x', Float), Column('y1', Float)]
        self.data_table = Table(self.table_name, self.metadata, *columns)

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        if len(row) != 2:
            raise ValueError("Incorrect number of columns in CSV row")
        return {
            'x': float(row[0]),
            'y1': float(row[1])
        }

class CSVLoader3(BaseCSVLoader):
    """
    Subclass of BaseCSVLoader for specific CSV files with 51 columns.

    Attributes:
        data_table: The SQLAlchemy table for the data.

    Methods:
        create_table: Method for creating the database table.
        extract_values: Method for extracting values from a row of the CSV file.
    """
    def create_table(self):
        """
        Creates the database table with 51 columns (x, y1, y2, ..., y50).
        """
        columns = [Column('x', Float)]
        columns += [Column(f'y{i}', Float) for i in range(1, 51)]  # Create 50 y-attributes
        self.data_table = Table(self.table_name, self.metadata, *columns)

    def extract_values(self, row):
        """
        Extracts values from a row of the CSV file.

        Parameters:
            row (list): The row of the CSV file as a list.

        Returns:
            dict: A dictionary containing the extracted values.
        """
        if len(row) != 51:
            raise ValueError("Incorrect number of columns in CSV row")
        values = {'x': float(row[0])}
        for i in range(1, 51):
            values[f'y{i}'] = float(row[i])
        return values

    




