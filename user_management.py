import bcrypt
import mysql.connector
from tkinter import messagebox

def register_user(username, password, first_name, last_name, email, connection):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor = connection.cursor()
    try:
        query = ("INSERT INTO users (username, password, firstName, lastName, email) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, (username, hashed, first_name, last_name, email))
        connection.commit()
        return "success"
    except mysql.connector.Error as err:
        if "Duplicate entry" in str(err) and "username" in str(err):
            return "duplicate_username"
        elif "Duplicate entry" in str(err) and "email" in str(err):
            return "duplicate_email"
        else:
            print(f"Registration error: {err}")
            return "error"
    finally:
        cursor.close()

def check_user(username, password, connection):
    cursor = connection.cursor()
    try:
        query = "SELECT username, password, firstName, lastName, email FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            return result
        return None
    except mysql.connector.Error as err:
        print(f"Login error: {err}")
        return None
    finally:
        cursor.close()

def validate_login(username, password, conn):
    user = check_user(username, password, conn)
    if user:
        return user
    else:
        messagebox.showerror("Error", "Invalid login credentials!")
        return None

def register_user_callback(username, password, password_confirm, first_name, last_name, email, conn):
    if password != password_confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return "mismatch_password"
    
    register_status = register_user(username, password, first_name, last_name, email, conn)
    if register_status == "success":
        messagebox.showinfo("Success", "Registration successful!")
    elif register_status == "duplicate_username":
        messagebox.showerror("Error", "Username already taken!")
    elif register_status == "duplicate_email":
        messagebox.showerror("Error", "Email already registered!")
    else:
        messagebox.showerror("Error", "An error occurred during registration!")
    
    return register_status
