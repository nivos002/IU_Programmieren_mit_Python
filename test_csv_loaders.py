import unittest
from csvloader import CSVLoader1, CSVLoader2, CSVLoader3

class TestCSVLoaders(unittest.TestCase):
    def setUp(self):
        # Initialize CSVLoader instances for testing
        self.loader1 = CSVLoader1(database_file='test.db', table_name='test_table_1')
        self.loader2 = CSVLoader2(database_file='test.db', table_name='test_table_2')
        self.loader3 = CSVLoader3(database_file='test.db', table_name='test_table_3')

    def test_create_table(self):
        # Test if the tables are created correctly
        self.loader1.create_table()
        self.assertTrue(self.loader1.engine.dialect.has_table(self.loader1.engine, self.loader1.table_name))
        
        self.loader2.create_table()
        self.assertTrue(self.loader2.engine.dialect.has_table(self.loader2.engine, self.loader2.table_name))
        
        self.loader3.create_table()
        self.assertTrue(self.loader3.engine.dialect.has_table(self.loader3.engine, self.loader3.table_name))

    def test_extract_values(self):
        # Test if the values are extracted correctly
        row1 = ['1.0', '2.0', '3.0', '4.0', '5.0']
        row2 = ['1.0', '2.0']
        row3 = ['1.0'] + ['2.0'] * 50
        
        self.assertEqual(self.loader1.extract_values(row1), {'x': 1.0, 'y1': 2.0, 'y2': 3.0, 'y3': 4.0, 'y4': 5.0})
        self.assertEqual(self.loader2.extract_values(row2), {'x': 1.0, 'y1': 2.0})
        self.assertEqual(self.loader3.extract_values(row3), {'x': 1.0, **{f'y{i}': 2.0 for i in range(1, 51)}})

    def tearDown(self):
        # Clean up after the tests
        self.loader1.conn.close()
        self.loader2.conn.close()
        self.loader3.conn.close()

if __name__ == '__main__':
    unittest.main()
