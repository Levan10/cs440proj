# phase2GUI.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess

# Modify start_phase2gui to accept the username argument
def start_phase2gui(logged_in_username):
    conn = sqlite3.connect('Rental_Units.db')
    cursor = conn.cursor()

    def search_units_by_feature(feature):
        cursor.execute("""
            SELECT unit_id, title, description, features, price, username 
            FROM rental_units 
            WHERE features LIKE ?
        """, ('%' + feature + '%',))
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
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a rental unit to review.")
            return

        selected_values = tree.item(selected_item, 'values')
        unit_id = selected_values[0]
        unit_title = selected_values[1]
        unit_owner = selected_values[5]  # Assuming 'username' is the sixth column

        # Pass username, unit_id, and title to the review interface
        subprocess.Popen(["python3", "phase2review.py", str(unit_id), unit_title, logged_in_username])

    root = tk.Tk()
    root.title("Rental Unit Feature Search")

    tk.Label(root, text="Feature:").grid(row=0, column=0)
    entry_feature = tk.Entry(root)
    entry_feature.grid(row=0, column=1)
    tk.Button(root, text="Search", command=on_search).grid(row=0, column=2)

    # Results table with an additional Username column
    columns = ("Unit ID", "Title", "Description", "Features", "Price", "Username")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=1, column=0, columnspan=4)

    tk.Button(root, text="Review", command=open_review_interface).grid(row=0, column=3)

    root.mainloop()
