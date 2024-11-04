import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

# Database Connection
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

def search_units_by_feature(feature):
    cursor.execute("SELECT title, description, features, price FROM rental_units WHERE features LIKE ?", ('%' + feature + '%',))
    results = cursor.fetchall()
    return results

def display_results(results):
    for row in tree.get_children():
        tree.delete(row)
    for row in results:
        tree.insert("", tk.END, values=row)

def on_search():
    feature = entry_feature.get()
    if not feature:
        messagebox.showerror("Input Error", "Please enter a feature to search.")
        return
    results = search_units_by_feature(feature)
    if results:
        display_results(results)
    else:
        messagebox.showinfo("No Results", "No rental units found with the specified feature.")

def open_review_interface():
    # Open review interface for the selected listing
    selected_item = tree.focus()  # Get the ID of the selected item in the treeview
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a rental unit to review.")
        return

    selected_values = tree.item(selected_item, 'values')
    title, description, features, price = selected_values  # Extract necessary data for review window

    # Pass the title as an argument to phase2review.py for displaying in the review interface
    subprocess.Popen(["python3", "phase2review.py", title])

# GUI setup
root = tk.Tk()
root.title("Rental Unit Feature Search")
root.geometry("900x700")

# Feature input and search button
tk.Label(root, text="Feature:").grid(row=0, column=0, padx=10, pady=10)
entry_feature = tk.Entry(root)
entry_feature.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Search", command=on_search).grid(row=0, column=2, padx=10, pady=10)

# Review button
review_button = tk.Button(root, text="Review", command=open_review_interface)
review_button.grid(row=0, column=3, padx=10, pady=10)

# Results table
columns = ("Title", "Description", "Features", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Close connection on close
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
