# Import necessary libraries for database connection
import mysql.connector
from mysql.connector import errorcode

def create_database_connection():
    """
    Create a connection to the MySQL database and return the connection object.
    
    Returns:
    - connection object if successful
    - None if an error occurs
    """
    try:
        # Establish a connection to the MySQL database using provided credentials and database name
        """
        connection = mysql.connector.connect(
            host='localhost',         # Server where the database is hosted
            user='root',              # Username to connect to the database
            password='CsunCS2023#',  # Password to connect to the database
            database='440phase2'       # Name of the database
        )


        """
        connection = mysql.connector.connect(
            host='localhost',         # Server where the database is hosted
            user='root',              # Username to connect to the database
            password='ClassOf2024!',  # Password to connect to the database
            database='project1'       # Name of the database
        )
        """
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Comp440$",
            database="testdatabase"
        )
        """
        return connection
    except mysql.connector.Error as err:
        # Handle specific errors
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            # Error due to invalid credentials
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # Error because the database specified does not exist
            print("Database does not exist")
        else:
            # Print any other error that might occur
            print(err)
    # Return None if connection was not established
    return None