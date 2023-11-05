import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from user_management import check_user, register_user
from item_management import InsertItemPage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Start Page", font=("Arial", 20)).pack(pady=10, padx=10)
        tk.Button(self, text="Login", font=("Arial", 16), width=20, command=lambda: self.controller.show_frame("LoginPage")).pack()
        tk.Button(self, text="Register", font=("Arial", 16), width=20, command=lambda: self.controller.show_frame("RegisterPage")).pack()

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
        tk.Button(self, text="Login", font=("Arial", 16), command=self.validate_login).pack()
        tk.Button(self, text="Back", font=("Arial", 16), command=lambda: self.controller.show_frame("StartPage")).pack()

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


class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Search Items by Category", font=("Arial", 20)).pack(pady=10, padx=10)
        self.category_entry = tk.Entry(self, font=("Arial", 16))
        self.category_entry.pack()
        tk.Button(self, text="Search", command=self.search_items).pack()
        tk.Button(self, text="Write Review", command=self.write_review).pack()

        self.result_tree = ttk.Treeview(self, columns=("ID", "Name", "Description", "Price", "Date"), show="headings")
        self.result_tree.heading("ID", text="ID")
        self.result_tree.heading("Name", text="Name")
        self.result_tree.heading("Description", text="Description")
        self.result_tree.heading("Price", text="Price")
        self.result_tree.heading("Date", text="Date")
        self.result_tree.pack(pady=10, padx=10)

        tk.Button(self, text="Back", command=lambda: self.controller.show_frame("LoggedInPage")).pack(pady=10)

    def search_items(self):
        category = self.category_entry.get()
        conn = self.controller.get_db_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT item_id, item_name, item_description, item_price, post_date FROM items WHERE category = %s"
            cursor.execute(query, (category,))
            results = cursor.fetchall()
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

    def display_results(self, results):
        self.result_tree.delete(*self.result_tree.get_children())
        if not results:
            self.result_tree.insert("", "end", values=("No items found for this category.", "", "", ""))
        else:
            for row in results:
                self.result_tree.insert("", "end", values=row)
    
    def write_review(self):
        selected_item = self.result_tree.focus()
        if selected_item == "":
            messagebox.showerror("Error", "No item selected")
            return
        item_details = self.result_tree.item(selected_item)['values']
        if item_details:
            self.controller.show_review_page(item_details[0])

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
        tk.Button(self, text="Search by Category", font=("Arial", 16), width=20, command=lambda: self.controller.show_frame("SearchPage")).pack()
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

    def search_items(self):
        category = self.category_entry.get()
        conn = self.controller.get_db_connection()
        cursor = conn.cursor()
        try:
            query = "SELECT item_id, item_name, item_description, item_price, post_date FROM items WHERE category = %s"
            cursor.execute(query, (category,))
            results = cursor.fetchall()
            self.controller.frames["SearchPage"].display_results(results)
            self.controller.show_frame("SearchPage")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()

    def logout(self):
        self.user = None
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.controller.show_frame("StartPage")

class ReviewPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.item_id = None  # This will be set when the page is shown
        self.create_widgets()

    def set_item_id(self, item_id):
        self.item_id = item_id

    def create_widgets(self):
        tk.Label(self, text="Write a Review", font=("Arial", 20)).pack(pady=10)
        tk.Label(self, text="Rating:", font=("Arial", 16)).pack()
        self.rating_var = tk.StringVar()
        self.rating_dropdown = tk.OptionMenu(self, self.rating_var, "excellent", "good", "fair", "poor")
        self.rating_dropdown.pack()

        tk.Label(self, text="Review:", font=("Arial", 16)).pack()
        self.review_text = tk.Text(self, height=4, width=50)
        self.review_text.pack()

        tk.Button(self, text="Submit Review", command=self.submit_review).pack()
    
    def submit_review(self):
        if not self.item_id:
            messagebox.showerror("Error", "Item not selected")
            return

        rating = self.rating_var.get()
        review = self.review_text.get("1.0", "end-1c")

        # Get the current user
        current_user = self.controller.frames["LoggedInPage"].user[0]  # Assuming the first element is the username

        # Start a connection to the database
        conn = self.controller.get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the item belongs to the user
            cursor.execute("SELECT username FROM items WHERE item_id = %s", (self.item_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Item not found")
                return
            if result[0] == current_user:
                messagebox.showwarning("Warning", "You cannot review your own item!")
                return

            # Check if the user has already submitted 3 reviews today
            cursor.execute("""
                SELECT COUNT(*) FROM reviews
                WHERE username = %s AND DATE(review_date) = CURDATE()
            """, (current_user,))
            review_count = cursor.fetchone()[0]
            if review_count >= 3:
                messagebox.showwarning("Warning", "You have already submitted 3 reviews today.")
                return

            # Insert the review
            cursor.execute("""
                INSERT INTO reviews (username, item_id, rating, description, review_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, (current_user, self.item_id, rating, review))
            conn.commit()
            messagebox.showinfo("Success", "Review submitted successfully!")

        except Exception as e:
            conn.rollback()  # Rollback the transaction on error
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            cursor.close()