import tkinter as tk
import tkinter.messagebox as messagebox

def insert_item_screen(app, username, conn):
    """
    Display the form for inserting a new item.
    """
    item_screen = tk.Frame(app)
    item_screen.grid(row=0, column=0, sticky="nsew")

    # Add labels and input fields for item details
    name_label = tk.Label(item_screen, text="Name:", font=("Arial", 16))
    name_label.grid(row=0, column=0, padx=10, pady=10)

    description_label = tk.Label(item_screen, text="Description:", font=("Arial", 16))
    description_label.grid(row=1, column=0, padx=10, pady=10)

    category_label = tk.Label(item_screen, text="Category:", font=("Arial", 16))
    category_label.grid(row=2, column=0, padx=10, pady=10)

    price_label = tk.Label(item_screen, text="Price:", font=("Arial", 16))
    price_label.grid(row=3, column=0, padx=10, pady=10)

    name_entry = tk.Entry(item_screen, font=("Arial", 16))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    description_entry = tk.Entry(item_screen, font=("Arial", 16))
    description_entry.grid(row=1, column=1, padx=10, pady=10)

    category_entry = tk.Entry(item_screen, font=("Arial", 16))
    category_entry.grid(row=2, column=1, padx=10, pady=10)

    price_entry = tk.Entry(item_screen, font=("Arial", 16))
    price_entry.grid(row=3, column=1, padx=10, pady=10)

    # Button to submit the item
    submit_button = tk.Button(item_screen, text="Submit", font=("Arial", 16), command=lambda: insert_new_item(username, name_entry.get(), description_entry.get(), category_entry.get(), price_entry.get(), conn))
    submit_button.grid(row=4, column=1, padx=10, pady=10)

def insert_new_item(username, name, description, category, price, conn):
    """
    Insert a new item into the database.
    """
    # TODO: Add logic to check if the user has added 3 items today.

    cursor = conn.cursor()
    try:
        query = "INSERT INTO items (username, item_name, item_description, category, item_price, post_date) VALUES (%s, %s, %s, %s, %s, CURDATE())"
        cursor.execute(query, (username, name, description, category, price))
        conn.commit()
        messagebox.showinfo("Success", "Item added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cursor.close()
