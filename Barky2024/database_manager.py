# database_manager.py
import sqlite3

class DatabaseManager:
    def __init__(self, database_filename):
        self.database_filename = database_filename
        self.connection = sqlite3.connect(database_filename)

    def does_table_exist(self, table_name):
        """Check if the specified table exists in the database."""
        cursor = self.connection.cursor()  # Create a cursor for this query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        exists = bool(cursor.fetchone())
        cursor.close()  # Close the cursor after its use
        return exists


    def close(self):
        self.connection.close()

    # Example method for creating a table
    def create_table(self, table_name, columns):
        columns_with_types = ', '.join([f"{column_name} {data_type}" for column_name, data_type in columns.items()])
        self.connection.execute(f"CREATE TABLE {table_name} ({columns_with_types})")
        self.connection.commit()

    # Example method for dropping a table
    def drop_table(self, table_name):
        self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    def does_table_exist(self, table_name):
        """Check if a table exists in the database."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name=?;
        """, (table_name,))
        return cursor.fetchone()[0] == 1

    # Add a method to get columns of a table if not exists
    def get_columns(self, table_name):
        """Get the column names of a table."""
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        # Extracting column names from the result
        columns = [info[1] for info in cursor.fetchall()]
        return columns

    # Implement other necessary database operations here...
