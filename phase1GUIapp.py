import tkinter as tk
from tkinter import messagebox
from phase1UserRegistration import signup, login
from phase1DataBase import create_table  # Import create_table function


# Function to handle user registration
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    phone = entry_phone.get()

    message = signup(username, password, confirm_password, first_name, last_name, email, phone)
    messagebox.showinfo("Signup", message)


# Function to handle user login
def login_user():
    username = entry_login_username.get()
    password = entry_login_password.get()

    message = login(username, password)
    messagebox.showinfo("Login", message)


# Setup Tkinter GUI
root = tk.Tk()
root.title("User Registration and Login")

# Set the window size to make it larger (e.g., 400x400 pixels)
root.geometry("700x600")

# Ensure the database table exists
create_table()

# Call create_table() to ensure the table is created before using it

# Registration form
tk.Label(root, text="Register", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Registration fields
tk.Label(root, text="Username").grid(row=1, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Password").grid(row=2, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Confirm Password").grid(row=3, column=0, padx=10, pady=5)
entry_confirm_password = tk.Entry(root, show='*')
entry_confirm_password.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="First Name").grid(row=4, column=0, padx=10, pady=5)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Last Name").grid(row=5, column=0, padx=10, pady=5)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=6, column=0, padx=10, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Phone").grid(row=7, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=7, column=1, padx=10, pady=5)

# Registration button
tk.Button(root, text="Register", command=register_user, width=15).grid(row=8, column=0, columnspan=2, pady=10)

# Login form
tk.Label(root, text="Login", font=("Arial", 16)).grid(row=9, column=0, columnspan=2, pady=10)

# Login fields
tk.Label(root, text="Username").grid(row=10, column=0, padx=10, pady=5)
entry_login_username = tk.Entry(root)
entry_login_username.grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Password").grid(row=11, column=0, padx=10, pady=5)
entry_login_password = tk.Entry(root, show='*')
entry_login_password.grid(row=11, column=1, padx=10, pady=5)

# Login button
tk.Button(root, text="Login", command=login_user, width=15).grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
