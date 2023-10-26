# Import necessary libraries for GUI and database operations
import tkinter as tk
import tkinter.messagebox as messagebox
from dbconnection import create_database_connection
from user_management import register_user, check_user
from item_management import insert_item_screen, insert_new_item


# Initialize the main application window
app = tk.Tk()
app.geometry("900x600")
app.title("Database Design Project")

# Ensure the main application window can grow/shrink
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Connect to the database
conn = create_database_connection()
if not conn:
    print("Error: Couldn't establish a connection to the database!")
    exit()

def start_screen():
    """Display the initial start screen with login and registration options."""
    start_frame = tk.Frame(app)
    start_frame.grid(row=0, column=0, sticky="nsew")

    # Configure grid layout for start frame
    start_frame.grid_rowconfigure(0, weight=1)
    start_frame.grid_rowconfigure(2, weight=1)
    start_frame.grid_columnconfigure(0, weight=1)
    start_frame.grid_columnconfigure(2, weight=1)

    # Add application label and login/register buttons
    app_label = tk.Label(start_frame, text="Database Design Project", font=("Arial", 20))
    app_label.grid(row=0, column=1, padx=10, pady=10)

    login_button = tk.Button(start_frame, text="Login", font=("Arial", 20), command=login)
    login_button.grid(row=1, column=0, padx=10, pady=10)

    register_button = tk.Button(start_frame, text="Register", font=("Arial", 20), command=register_screen)
    register_button.grid(row=1, column=2, padx=10, pady=10)

def validate_login():
    """Authenticate user's credentials and navigate to logged-in screen if successful."""
    username = username_entry.get()
    password = password_entry.get()

    user = check_user(username, password, conn)
    
    if user:
        for widget in app.winfo_children():
            widget.destroy()
        logged_in_screen(user)
    else:
        messagebox.showerror("Error", "Invalid login credentials!")

def back_to_start():
    """Clear all widgets and navigate back to the main start screen."""
    for widget in app.winfo_children():
        widget.destroy()
    start_screen()

def register_user_callback():
    """Handle user registration process and notify the user of the result."""
    username = username_entry.get()
    password = password_entry.get()
    password_confirm = password_confirm_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()

    if password != password_confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    register_status = register_user(username, password, first_name, last_name, email, conn)
    if register_status == "success":
        messagebox.showinfo("Success", "Registration successful!")
        for widget in app.winfo_children():
            widget.destroy()
        logged_in_screen((username, password, first_name, last_name, email))
    elif register_status == "duplicate_username":
        messagebox.showerror("Error", "Username already taken!")
    elif register_status == "duplicate_email":
        messagebox.showerror("Error", "Email already registered!")
    else:
        messagebox.showerror("Error", "An error occurred during registration!")

def logged_in_screen(user):
    """Display a welcome message for the logged-in user and provide options for further actions."""
    logged_in_frame = tk.Frame(app)
    logged_in_frame.grid(row=0, column=0, sticky="nsew")

    # Grid layout for the frame
    logged_in_frame.grid_rowconfigure(0, weight=1)
    logged_in_frame.grid_columnconfigure(0, weight=1)

    welcome_label = tk.Label(logged_in_frame, text=f"Welcome {user[2]} {user[3]}", font=("Arial", 20))
    welcome_label.grid(row=0, column=0, padx=10, pady=10)

    # Insert Item button
    insert_item_button = tk.Button(logged_in_frame, text="Insert New Item", font=("Arial", 16), command=lambda: insert_item_screen(app, user[0], conn))
    insert_item_button.grid(row=1, column=0, padx=10, pady=10)

    # Log Out button
    logout_button = tk.Button(logged_in_frame, text="Log Out", font=("Arial", 16), command=logout)
    logout_button.grid(row=2, column=0, padx=10, pady=10)

def logout():
    """log out and return to the start screen."""
    for widget in app.winfo_children():
        widget.destroy()
    start_screen()

def login():
    """Display the login screen."""
    login_screen = tk.Frame(app)
    login_screen.grid(row=0, column=0, sticky="nsew")

    # Configure grid layout for the login screen
    login_screen.grid_rowconfigure(0, weight=1)
    login_screen.grid_rowconfigure(2, weight=1)
    login_screen.grid_columnconfigure(0, weight=1)
    login_screen.grid_columnconfigure(2, weight=1)

    # Add labels, input fields, and buttons
    login_label = tk.Label(login_screen, text="Database Design Project", font=("Arial", 20))
    login_label.grid(row=0, column=1, padx=10, pady=10)

    username_label = tk.Label(login_screen, text="Username:", font=("Arial", 16))
    username_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tk.Label(login_screen, text="Password:", font=("Arial", 16))
    password_label.grid(row=2, column=0, padx=10, pady=10)

    global username_entry
    username_entry = tk.Entry(login_screen, font=("Arial", 16))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    global password_entry
    password_entry = tk.Entry(login_screen, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    login_button = tk.Button(login_screen, text="Login", font=("Arial", 20), command=validate_login)
    login_button.grid(row=3, column=1, padx=10, pady=10)
    
    back_button = tk.Button(login_screen, text="Back", font=("Arial", 16), command=back_to_start)
    back_button.grid(row=4, column=1, padx=10, pady=10)

def register_screen():
    """Display the registration screen for users to sign up."""
    register_frame = tk.Frame(app)
    register_frame.grid(row=0, column=0, sticky="nsew")

    # Configure grid layout for the registration screen
    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_rowconfigure(7, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)
    register_frame.grid_columnconfigure(2, weight=1)

    # Add labels, input fields, and buttons
    register_label = tk.Label(register_frame, text="Register", font=("Arial", 20))
    register_label.grid(row=0, column=1, padx=10, pady=10)

    username_label = tk.Label(register_frame, text="Username:", font=("Arial", 16))
    username_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tk.Label(register_frame, text="Password:", font=("Arial", 16))
    password_label.grid(row=2, column=0, padx=10, pady=10)

    password_confirm_label = tk.Label(register_frame, text="Confirm Password:", font=("Arial", 16))
    password_confirm_label.grid(row=3, column=0, padx=10, pady=10)

    first_name_label = tk.Label(register_frame, text="First Name:", font=("Arial", 16))
    first_name_label.grid(row=4, column=0, padx=10, pady=10)

    last_name_label = tk.Label(register_frame, text="Last Name:", font=("Arial", 16))
    last_name_label.grid(row=5, column=0, padx=10, pady=10)

    email_label = tk.Label(register_frame, text="Email:", font=("Arial", 16))
    email_label.grid(row=6, column=0, padx=10, pady=10)

    global username_entry
    username_entry = tk.Entry(register_frame, font=("Arial", 16))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    global password_entry
    password_entry = tk.Entry(register_frame, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    global password_confirm_entry
    password_confirm_entry = tk.Entry(register_frame, show="*", font=("Arial", 16))
    password_confirm_entry.grid(row=3, column=1, padx=10, pady=10)

    global first_name_entry
    first_name_entry = tk.Entry(register_frame, font=("Arial", 16))
    first_name_entry.grid(row=4, column=1, padx=10, pady=10)

    global last_name_entry
    last_name_entry = tk.Entry(register_frame, font=("Arial", 16))
    last_name_entry.grid(row=5, column=1, padx=10, pady=10)

    global email_entry
    email_entry = tk.Entry(register_frame, font=("Arial", 16))
    email_entry.grid(row=6, column=1, padx=10, pady=10)

    register_button = tk.Button(register_frame, text="Register", font=("Arial", 20), command=register_user_callback)
    register_button.grid(row=7, column=1, padx=10, pady=10)

    back_button = tk.Button(register_frame, text="Back", font=("Arial", 16), command=back_to_start)
    back_button.grid(row=8, column=1, padx=10, pady=10)

# Begin the GUI application by displaying the main start screen
start_screen()
app.mainloop()
