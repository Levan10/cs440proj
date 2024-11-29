import tkinter as tk
from tkinter import messagebox
from phase1UserRegistration import signup, login
from MainDataBase import create_tables
from phase3GUI import start_phase2gui  # Ensure start_phase2gui accepts the username argument

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

# Update login function to pass username to phase2


def login_user():
    username = entry_login_username.get()
    password = entry_login_password.get()
    message = login(username, password)
    messagebox.showinfo("Login", message)

    if message == "Login successful!":
        root.destroy()
        start_phase2gui(username)  # Pass username to phase2

# GUI setup
root = tk.Tk()
root.title("User Registration and Login")
root.geometry("700x600")

# Ensure the database table exists
create_tables()

# Registration form
tk.Label(root, text="Register", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Entry fields for registration
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show='*')
entry_confirm_password = tk.Entry(root, show='*')
entry_first_name = tk.Entry(root)
entry_last_name = tk.Entry(root)
entry_email = tk.Entry(root)
entry_phone = tk.Entry(root)

# Create input fields
fields = ["Username:", "Password:", "Confirm Password:", "First Name:", "Last Name:", "Email:", "Phone:"]
entries = [entry_username, entry_password, entry_confirm_password, entry_first_name, entry_last_name, entry_email, entry_phone]

# Loop to create labels and place them in a grid layout with their corresponding entry fields
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i + 1, column=0)
    entries[i].grid(row=i + 1, column=1)

# Registration button
tk.Button(root, text="Register", command=register_user, width=15).grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

# Login form
tk.Label(root, text="Login", font=("Arial", 16)).grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

entry_login_username = tk.Entry(root)
entry_login_password = tk.Entry(root, show='*')

tk.Label(root, text="Username:").grid(row=len(fields) + 3, column=0)
entry_login_username.grid(row=len(fields) + 3, column=1)

tk.Label(root, text="Password:").grid(row=len(fields) + 4, column=0)
entry_login_password.grid(row=len(fields) + 4, column=1)

# Login button
tk.Button(root, text="Login", command=login_user, width=15).grid(row=len(fields) + 5, column=0, columnspan=2, pady=10)

root.mainloop()
