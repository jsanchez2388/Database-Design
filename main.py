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

    login_button = tk.Button(login_screen, text="Login", font=("Arial", 20))
    login_button.grid(row=1, column=1, padx=10, pady=10)

login()

#Run App
app.mainloop()