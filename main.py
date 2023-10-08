import tkinter as tk
import mysql.connector

app = tk.Tk()
app.geometry("900x600")
app.title("Database Design Project")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Comp440$",
    database="testdatabase"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM users")

# Fetch and print the results
for row in cursor.fetchall():
    print(row)
def insert_test_user():
    # Test user data
    test_user_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'firstName': 'Test',
        'lastName': 'User',
        'email': 'testuser@example.com'
    }

    # Insert test user data into the database
    insert_query = """
        INSERT INTO users (username, password, firstName, lastName, email)
        VALUES (%(username)s, %(password)s, %(firstName)s, %(lastName)s, %(email)s)
    """
    cursor.execute(insert_query, test_user_data)
    conn.commit()

def login():
    def validate_login():
        username = student_id_entry.get()
        password = password_entry.get()

        # Check user credentials in the database
        cursor.execute('''
            SELECT * FROM users WHERE username = %s AND password = %s
        ''', (username, password))
        user = cursor.fetchone()

        if user:
            login_screen.destroy()  # Destroy the login screen
            logged_in_screen(user)
        else:
            logged_in_label.config(text="Login failed. Invalid credentials.")

    def destroy_login_screen():
        login_screen.destroy()

    def logged_in_screen(user):
        logged_in_frame = tk.Frame(app)
        logged_in_frame.grid(row=0, column=0, sticky="nsew")

        logged_in_frame.grid_rowconfigure(0, weight=1)
        logged_in_frame.grid_columnconfigure(0, weight=1)

        welcome_label = tk.Label(logged_in_frame, text=f"Welcome {user[2]} {user[3]}", font=("Arial", 20))
        welcome_label.grid(row=0, column=0, padx=10, pady=10)
    login_screen = tk.Frame(app)
    login_screen.grid(row=0, column=0, sticky="nsew")

    login_screen.grid_rowconfigure(0, weight=1)
    login_screen.grid_rowconfigure(2, weight=1)
    login_screen.grid_columnconfigure(0, weight=1)
    login_screen.grid_columnconfigure(2, weight=1)

    login_label = tk.Label(login_screen, text="Database Design Project", font=("Arial", 20))
    login_label.grid(row=0, column=1, padx=10, pady=10)

    student_id_label = tk.Label(login_screen, text="Username:", font=("Arial", 16))
    student_id_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tk.Label(login_screen, text="Password:", font=("Arial", 16))
    password_label.grid(row=2, column=0, padx=10, pady=10)

    student_id_entry = tk.Entry(login_screen, font=("Arial", 16))
    student_id_entry.grid(row=1, column=1, padx=10, pady=10)

    password_entry = tk.Entry(login_screen, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    login_button = tk.Button(login_screen, text="Login", font=("Arial", 20),command=validate_login)
    login_button.grid(row=3, column=1, padx=10, pady=10)

    logged_in_label = tk.Label(login_screen, text="", font=("Arial", 16))
    logged_in_label.grid(row=4, column=1, padx=10, pady=10)


def register_screen():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()

        # Check if username and email are unique
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_username = cursor.fetchone()

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        existing_email = cursor.fetchone()

        if existing_username:
            registration_status_label.config(text="Registration failed. Username already exists.")
        elif existing_email:
            registration_status_label.config(text="Registration failed. Email already exists.")
        elif password != password_confirm:
            registration_status_label.config(text="Registration failed. Passwords do not match.")
        else:
            # Insert user data into the MySQL database
            insert_query = """
                INSERT INTO users (username, password, firstName, lastName, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (username, password, first_name, last_name, email)
            cursor.execute(insert_query, values)
            conn.commit()

            registration_status_label.config(text=f"User '{first_name} {last_name}' is registered and logged in.")

    register_frame = tk.Frame(app)
    register_frame.grid(row=0, column=0, sticky="nsew")

    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_rowconfigure(9, weight=1)
    register_frame.grid_columnconfigure(0, weight=1)
    register_frame.grid_columnconfigure(2, weight=1)

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

    username_entry = tk.Entry(register_frame, font=("Arial", 16))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_entry = tk.Entry(register_frame, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    password_confirm_entry = tk.Entry(register_frame, show="*", font=("Arial", 16))
    password_confirm_entry.grid(row=3, column=1, padx=10, pady=10)

    first_name_entry = tk.Entry(register_frame, font=("Arial", 16))
    first_name_entry.grid(row=4, column=1, padx=10, pady=10)

    last_name_entry = tk.Entry(register_frame, font=("Arial", 16))
    last_name_entry.grid(row=5, column=1, padx=10, pady=10)

    email_entry = tk.Entry(register_frame, font=("Arial", 16))
    email_entry.grid(row=6, column=1, padx=10, pady=10)

    register_button = tk.Button(register_frame, text="Register", font=("Arial", 20), command=register_user)
    register_button.grid(row=7, column=1, padx=10, pady=10)

    registration_status_label = tk.Label(register_frame, text="", font=("Arial", 16))
    registration_status_label.grid(row=8, column=1, padx=10, pady=10)


def start_screen():
    start_frame = tk.Frame(app)
    start_frame.grid(row=0, column=0, sticky="nsew")

    start_frame.grid_rowconfigure(0, weight=1)
    start_frame.grid_rowconfigure(2, weight=1)
    start_frame.grid_columnconfigure(0, weight=1)
    start_frame.grid_columnconfigure(2, weight=1)

    app_label = tk.Label(start_frame, text="Database Design Project", font=("Arial", 20))
    app_label.grid(row=0, column=1, padx=10, pady=10)

    login_button = tk.Button(start_frame, text="Login", font=("Arial", 20), command=login)
    login_button.grid(row=1, column=0, padx=10, pady=10)

    register_button = tk.Button(start_frame, text="Register", font=("Arial", 20), command=register_screen)
    register_button.grid(row=1, column=2, padx=10, pady=10)


start_screen()


#Run App
app.mainloop()