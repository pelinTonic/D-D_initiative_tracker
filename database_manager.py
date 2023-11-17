import sqlite3
from error_handling import *

def create_connection(db_file: str) -> sqlite3:

    """takes a single argument db_file, which is expected to be a string 
        representing the path to an SQLite database file. The purpose of this function is to create a 
        connection to an SQLite database and return that connection object.

    Args:
        db_file (str): name of the database

    Returns:
        sqlite3: connection object
    """
    sql_connection = None

    try:
        sql_connection = sqlite3.connect(db_file)
        return sql_connection

    except sqlite3.Error as error:
        print(f"Greška kod kreiranja baze - {error}")
        return sql_connection
    


def create_table(sql_connection: sqlite3.Connection, create_table_sql: str) -> bool:

    """takes two arguments: sql_connection, which is expected to be a valid SQLite database connection, 
    and create_table_sql, which is a SQL statement for creating the table. The function returns a Boolean value, 
    True if the table creation is successful, and False if there is an error.

    Args:
        sql_connection (sqlite3.Connection): valid SQLite database connection
        create_table_sql (str): SQL statement for creating the table

    Returns:
        bool: _description_
    """
    try:
        cursor = sql_connection.cursor()
        cursor.execute(create_table_sql)
        sql_connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as error:
        print(f"Greška kod kreiranja tablice - {error}")
        return False
    
def insert_into_table(
    sql_connection: sqlite3.Connection, 
    insert_sql: str,
    data: tuple
) -> bool:
    
    """Inserting data into an SQLite database table using a provided SQL insertion 
        statement and a list of data. It returns a Boolean value to indicate the success or 
        failure of the insertion operation.

    Args:
        sql_connection (sqlite3.Connection):  A valid SQLite database connection
        insert_sql (str): The SQL statement used to insert data into the table.
        data (list): A list of data items to be inserted into the table using the insert_sql statement.

    Returns:
        bool: Returns a boolean value indicating the success or failure of 
        the insertion operation. 
    """
    try:
        cursor = sql_connection.cursor()
        cursor.execute(insert_sql, data)
        sql_connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as error:
        print(f"Greška kod umetanja u tablicu - {error}")
        return False
    
def get_row_number(sql_connection: sqlite3.Connection, table_name: str) -> int :

    """Retrieve the number of rows (records) in a specified SQLite database table

    Args:
        sql_connection (sqlite3.Connection): A valid SQLite database connection that allows interaction with the database.
        table_name (str): The name of the table for which you want to count the rows.

    Returns:
        int: Number of rows
    """

    try:
        cursor = sql_connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        return row_count
    except sqlite3.Error as error:
        print(f"Greška - {error} ")


def get_largest_ID(sql_connection: sqlite3.Connection, table_name: str) -> int:

    try:
        cursor = sql_connection.cursor()
        cursor.execute(f"SELECT MAX(number) FROM {table_name}")
        max_number = cursor.fetchone()[0]
        return max_number
    except sqlite3.Error as error:
        print(f"Greška - {error} ")


def select_data_from_database(database_name: str, table_name: str) -> tuple:
    
    """ retrieve all data (all rows and columns) from a specified SQLite database table.

    Args:
        database_name (str): The name of the SQLite database file from which you want to retrieve data.
        table_name (str): The name of the table from which you want to select data.

    Returns:
        tuple: result
    """
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    result = cursor.fetchall()
    
    return result

def delete_from_database(number: int, database_name: str, table_name: str):

    """
    Delete a record from an SQLite database table.

    Args:
        number (int): The value to match for deleting a record.
        database_name (str): The name of the SQLite database file.
        table_name (str): The name of the table to delete from.

    Returns:
        None

    Raises:
        Exception: If there is an error during the deletion operation, an exception is raised.

    This function connects to the specified SQLite database, executes a DELETE SQL
    statement to remove a record from the specified table where the 'number' column
    matches the provided number, and commits the changes to the database.

    If an exception occurs during the database operation, an error message is printed.

    """
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE number = ?", (number,))
        conn.commit()
        cursor.close()
        conn.close()

    except sqlite3.Error as error:
        data_entry_error(error)


def update_database(name: str, database_name: str, table_name: str, hp: int, condition: str):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET hp = ? WHERE name = ?", (hp,name))
        cursor.execute(f"UPDATE {table_name} SET condition = ? WHERE name = ?", (condition,name))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as error:
        data_entry_error(error)
        


# conn = create_connection("initiative_tracker.db")
# print(get_row_number(conn, "initiative"))
# result = select_data_from_database("initiative_tracker.db", "initiative")
# print(result)