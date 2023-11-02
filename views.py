import tkinter as tk
from tkinter import messagebox
from user_management import check_user, register_user
from item_management import InsertItemPage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Start Page", font=("Arial", 20)).pack(pady=10, padx=10)
        tk.Button(self, text="Login", width=20, command=lambda: self.controller.show_frame("LoginPage")).pack()
        tk.Button(self, text="Register", width=20, command=lambda: self.controller.show_frame("RegisterPage")).pack()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=10, padx=10)
        self.username_entry = tk.Entry(self, font=("Arial", 16))
        self.username_entry.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.pack()
        tk.Button(self, text="Login", command=self.validate_login).pack()
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage")).pack()

    def validate_login(self):
        conn = self.controller.get_db_connection()
        user = check_user(self.username_entry.get(), self.password_entry.get(), conn)
        if user:
            self.controller.frames[LoggedInPage.__name__].set_user(user)
            self.controller.show_frame("LoggedInPage")
        else:
            messagebox.showerror("Error", "Invalid login credentials!")

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Register", font=("Arial", 20)).pack(pady=(10, 0), padx=10)
        
        tk.Label(self, text="Username:", font=("Arial", 16)).pack(pady=(10, 0))
        self.username_entry = tk.Entry(self, font=("Arial", 16))
        self.username_entry.pack()
        
        tk.Label(self, text="Password:", font=("Arial", 16)).pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_entry.pack()
        
        tk.Label(self, text="Confirm Password:", font=("Arial", 16)).pack(pady=(10, 0))
        self.password_confirm_entry = tk.Entry(self, show="*", font=("Arial", 16))
        self.password_confirm_entry.pack()
        
        tk.Label(self, text="First Name:", font=("Arial", 16)).pack(pady=(10, 0))
        self.first_name_entry = tk.Entry(self, font=("Arial", 16))
        self.first_name_entry.pack()
        
        tk.Label(self, text="Last Name:", font=("Arial", 16)).pack(pady=(10, 0))
        self.last_name_entry = tk.Entry(self, font=("Arial", 16))
        self.last_name_entry.pack()
        
        tk.Label(self, text="Email:", font=("Arial", 16)).pack(pady=(10, 0))
        self.email_entry = tk.Entry(self, font=("Arial", 16))
        self.email_entry.pack()
        
        tk.Button(self, text="Register", command=self.register_user_callback).pack(pady=(10, 0))
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("StartPage")).pack(pady=(10, 20))

    def register_user_callback(self):
        conn = self.controller.get_db_connection()
        status = register_user(
            self.username_entry.get(),
            self.password_entry.get(),
            self.first_name_entry.get(),
            self.last_name_entry.get(),
            self.email_entry.get(),
            conn
        )
        if status == "success":
            messagebox.showinfo("Success", "Registration successful!")
            self.controller.show_frame("LoginPage")
        elif status == "duplicate_username":
            messagebox.showerror("Error", "Username already taken!")
        elif status == "duplicate_email":
            messagebox.showerror("Error", "Email already registered!")
        else:
            messagebox.showerror("Error", "An error occurred during registration!")

class LoggedInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user = None
        self.create_widgets()

    def create_widgets(self):
        self.welcome_label = tk.Label(self, font=("Arial", 20))
        self.welcome_label.pack(pady=10, padx=10)
        tk.Button(self, text="Insert New Item", font=("Arial", 16), command=self.insert_item).pack()
        tk.Button(self, text="Log Out", font=("Arial", 16), command=self.logout).pack()

    def set_user(self, user):
        self.user = user
        self.welcome_label.config(text=f"Welcome {user[2]} {user[3]}")

    def insert_item(self):
        # Check if the user has added 3 items today
        conn = self.controller.get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
            SELECT COUNT(*) FROM items 
            WHERE username = %s AND DATE(post_date) = CURDATE()
            """
            cursor.execute(query, (self.user[0],))
            result = cursor.fetchone()
            if result[0] >= 3:
                messagebox.showwarning("Limit Reached", "You have already added 3 items today.")
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        finally:
            cursor.close()

        # Set the username in the InsertItemPage
        self.controller.frames[InsertItemPage.__name__].set_username(self.user[0])
        # Show the InsertItemPage
        self.controller.show_frame("InsertItemPage")

    def logout(self):
        self.user = None
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.controller.show_frame("StartPage")
