# Import necessary libraries for password hashing and database connection
import bcrypt
import mysql.connector

def register_user(username, password, first_name, last_name, email, connection):
    """
    Register a new user in the database.
    
    Parameters:
    - username: Username of the user.
    - password: Plain-text password of the user.
    - first_name: First name of the user.
    - last_name: Last name of the user.
    - email: Email address of the user.
    - connection: Active database connection object.
    
    Returns:
    - "success" if registration was successful.
    - "duplicate_username" if username already exists.
    - "duplicate_email" if email already exists.
    - "error" for any other error.
    """
    # Convert the plain-text password into a hashed version using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = connection.cursor()
    try:
        # SQL query to insert the new user's details into the 'users' table
        query = ("INSERT INTO users (username, password, firstName, lastName, email) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, (username, hashed, first_name, last_name, email))
        connection.commit()
        return "success"
    except mysql.connector.Error as err:
        # Handle specific error messages related to duplicate entries
        if "Duplicate entry" in str(err) and "username" in str(err):
            return "duplicate_username"
        elif "Duplicate entry" in str(err) and "email" in str(err):
            return "duplicate_email"
        else:
            # For any other error, return a generic "error" message
            return "error"
    finally:
        # Close the database cursor
        cursor.close()

def check_user(username, password, connection):
    cursor = connection.cursor()
    try:
        # SQL query to fetch the user details for the given username
        query = "SELECT username, password, firstName, lastName, email FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            stored_password = result[1]
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return result
        return None
    except mysql.connector.Error as err:
        # Print the error and return None
        print(err)
        return None
    finally:
        # Close the database cursor
        cursor.close()
