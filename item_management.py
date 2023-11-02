import tkinter as tk
import tkinter.messagebox as messagebox

class InsertItemPage(tk.Frame):
    def __init__(self, parent, controller, on_item_inserted_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.on_item_inserted_callback = on_item_inserted_callback
        self.username = None  # This will be set when the page is shown

        # Add labels and input fields for item details
        name_label = tk.Label(self, text="Name:", font=("Arial", 16))
        name_label.grid(row=0, column=0, padx=10, pady=10)

        description_label = tk.Label(self, text="Description:", font=("Arial", 16))
        description_label.grid(row=1, column=0, padx=10, pady=10)

        category_label = tk.Label(self, text="Category:", font=("Arial", 16))
        category_label.grid(row=2, column=0, padx=10, pady=10)

        price_label = tk.Label(self, text="Price:", font=("Arial", 16))
        price_label.grid(row=3, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self, font=("Arial", 16))
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.description_entry = tk.Entry(self, font=("Arial", 16))
        self.description_entry.grid(row=1, column=1, padx=10, pady=10)

        self.category_entry = tk.Entry(self, font=("Arial", 16))
        self.category_entry.grid(row=2, column=1, padx=10, pady=10)

        self.price_entry = tk.Entry(self, font=("Arial", 16))
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        # Button to submit the item
        submit_button = tk.Button(self, text="Submit", font=("Arial", 16),
                                  command=self.insert_new_item)
        submit_button.grid(row=4, column=1, padx=10, pady=10)

    def set_username(self, username):
        self.username = username

    def insert_new_item(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        category = self.category_entry.get()
        price = self.price_entry.get()
        conn = self.controller.conn

        cursor = conn.cursor()
        try:
            query = "INSERT INTO items (username, item_name, item_description, category, item_price, post_date) VALUES (%s, %s, %s, %s, %s, CURDATE())"
            cursor.execute(query, (self.username, name, description, category, price))
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully!")
            if self.on_item_inserted_callback:
                self.on_item_inserted_callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
