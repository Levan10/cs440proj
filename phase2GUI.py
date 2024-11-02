import tkinter as tk
from tkinter import messagebox, ttk
from phase2User import insert_unit
from phase2DataBase import create_tables

# Initialize database tables
create_tables()  # Ensures tables are created at the start of the program

# Function to handle adding a rental unit by calling insert_unit
def add_unit():
        try:
            # Ensure the Username field is not empty
            if not entry_username.get():
                messagebox.showerror("Input Error", "Username cannot be empty.")
                return

            username = entry_username.get()  # Get username from the entry field
            title = entry_title.get()  # Get title input from the entry field
            description = entry_description.get()  # Get description input from the entry field
            features = entry_features.get()  # Get features input from the entry field
            price = float(entry_price.get())  # Get price input from the entry field, converting it to a float

            result = insert_unit(username, title, description, features,
                                 price)  # Call the function to insert rental unit data
            messagebox.showinfo("Add Rental Unit", result)  # Show a message box with the result of the operation

        except ValueError:
            messagebox.showerror("Input Error",
                                 "Please enter valid numbers for Price.")  # Handle invalid input

# This portion of the code is responsible for the GUI

root = tk.Tk()
root.title("Rental Unit System")

# GUI layout for the "Add Rental Unit" section
tk.Label(root, text="Add Rental Unit").grid(row=0, column=0, columnspan=2)  # Label for section title

# Creating entry fields for user input
entry_username = tk.Entry(root)  # Entry for username
entry_title = tk.Entry(root)  # Entry for title
entry_description = tk.Entry(root)  # Entry for description
entry_features = tk.Entry(root)  # Entry for features
entry_price = tk.Entry(root)  # Entry for price

# List of field labels and entry widgets for simplified layout generation
fields = ["Username:", "Title:", "Description:", "Features:", "Price:"]
entries = [entry_username, entry_title, entry_description, entry_features, entry_price]

# Loop to create labels and place them in a grid layout with their corresponding entry fields
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i+1, column=0)
    entries[i].grid(row=i+1, column=1)

# Button to submit the form and add the rental unit, calling add_unit when clicked
tk.Button(root, text="Add Unit", command=add_unit).grid(row=len(fields) + 1, column=0, columnspan=2)

root.geometry("700x600")
root.mainloop()
