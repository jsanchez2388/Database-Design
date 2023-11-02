import tkinter as tk
from tkinter import messagebox
from dbconnection import create_database_connection
from views import StartPage, LoginPage, RegisterPage, LoggedInPage
from item_management import InsertItemPage

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("900x600")
        self.title("Database Design Project")
        self.conn = create_database_connection()
        if not self.conn:
            messagebox.showerror("Error", "Couldn't establish a connection to the database!")
            self.quit()
            return

        # Container to hold all the frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LoginPage, RegisterPage, LoggedInPage, InsertItemPage):
            page_name = F.__name__  # Use the class name as a string
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame  # Use the class name string as the key
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        # Create InsertItemPage separately to pass the callback
        self.frames[InsertItemPage.__name__] = InsertItemPage(parent=container, controller=self, on_item_inserted_callback=self.show_logged_in_frame)
        self.frames[InsertItemPage.__name__].grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_logged_in_frame(self):
        """Callback function to show the LoggedInPage."""
        self.show_frame("LoggedInPage")

    def get_db_connection(self):
        return self.conn

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
