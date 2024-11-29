import tkinter as tk
from tkinter import messagebox
from phase2User import insert_unit
from MainDataBase import create_tables
import subprocess

# Initialize database tables
create_tables()

# Define the logout function to close the current window and open phase1GUIapp
def logout(root):
    root.destroy()  # Close the current window
    subprocess.Popen(["python3", "phase1GUIapp.py"])  # Open the phase1 GUI

# Function to open the search interface
def open_search_interface(username):
    subprocess.Popen(["python3", "phase3SearchInterface.py", username])  # Pass the username

# Modify the add_unit function to use the logged-in username from Phase 1
def add_unit(username):
    try:
        # Ensure that entry fields are declared globally
        global entry_title, entry_description, entry_features, entry_price

        title = entry_title.get()
        description = entry_description.get()
        features = entry_features.get()
        price = float(entry_price.get())

        result = insert_unit(username, title, description, features, price)
        messagebox.showinfo("Add Rental Unit", result)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for Price.")

# GUI layout
def start_phase2gui(username):
    global entry_title, entry_description, entry_features, entry_price  # Declare as global here

    root = tk.Tk()
    root.title("Rental Unit System")

    # GUI layout for "Add Rental Unit"
    tk.Label(root, text="Add Rental Unit").grid(row=0, column=0, columnspan=2)

    # Creating entry fields for user input
    entry_title = tk.Entry(root)
    entry_description = tk.Entry(root)
    entry_features = tk.Entry(root)
    entry_price = tk.Entry(root)

    fields = ["Title:", "Description:", "Features:", "Price:"]
    entries = [entry_title, entry_description, entry_features, entry_price]

    # Grid layout for labels and entries
    for i, field in enumerate(fields):
        tk.Label(root, text=field).grid(row=i + 1, column=0)
        entries[i].grid(row=i + 1, column=1)

    # Add unit button (using the logged-in username)
    tk.Button(root, text="Add Unit", command=lambda: add_unit(username)).grid(row=len(fields) + 1, column=0,
                                                                              columnspan=2)
    # Update the search button to pass the username
    tk.Button(root, text="Search for Unit", command=lambda: open_search_interface(username)).grid(row=len(fields) + 2, column=0,
                                                                                columnspan=2)

    # Logout button
    tk.Button(root, text="Logout", command=lambda: logout(root)).grid(row=len(fields) + 3, column=0, columnspan=2)

    root.geometry("700x600")
    root.mainloop()
