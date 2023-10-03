import tkinter as tk

app = tk.Tk()
app.geometry("900x600")
app.title("Database Design Project")

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)


def login():
    login_screen = tk.Frame(app)
    login_screen.grid(row=0, column=0, sticky="nsew")

    login_screen.grid_rowconfigure(0, weight=1)
    login_screen.grid_rowconfigure(2, weight=1)
    login_screen.grid_columnconfigure(0, weight=1)
    login_screen.grid_columnconfigure(2, weight=1)

    login_label = tk.Label(login_screen, text="Database Design Project", font=("Arial", 20))
    login_label.grid(row=0, column=1, padx=10, pady=10)

    student_id_label = tk.Label(login_screen, text="Student ID:", font=("Arial", 16))
    student_id_label.grid(row=1, column=0, padx=10, pady=10)

    password_label = tk.Label(login_screen, text="Password:", font=("Arial", 16))
    password_label.grid(row=2, column=0, padx=10, pady=10)

    student_id_entry = tk.Entry(login_screen, font=("Arial", 16))
    student_id_entry.grid(row=1, column=1, padx=10, pady=10)

    password_entry = tk.Entry(login_screen, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    login_button = tk.Button(login_screen, text="Login", font=("Arial", 20))
    login_button.grid(row=3, column=1, padx=10, pady=10)

def register_screen():
    register_frame = tk.Frame(app)
    register_frame.grid(row=0, column=0, sticky="nsew")

    register_frame.grid_rowconfigure(0, weight=1)
    register_frame.grid_rowconfigure(7, weight=1)
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

    register_button = tk.Button(register_frame, text="Register", font=("Arial", 20),)
    register_button.grid(row=7, column=1, padx=10, pady=10)

def logged_in_screen():
    logged_in_frame = tk.Frame(app)
    logged_in_frame.grid(row=0, column=0, sticky="nsew")

    logged_in_frame.grid_rowconfigure(0, weight=1)
    logged_in_frame.grid_columnconfigure(0, weight=1)

    logged_in_label = tk.Label(logged_in_frame, text=f"User 'John Doe' is logged in", font=("Arial", 20))
    logged_in_label.grid(row=0, column=0, padx=10, pady=10)
# login()
# register_screen()
logged_in_screen()
#Run App
app.mainloop()