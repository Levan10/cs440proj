import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

#Database Connection
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

def search_units_by_feature(feature):
    """ Type in a Rental Unit Feature """
    cursor.execute("SELECT title, description, features, price FROM rental_units WHERE features LIKE ?", ('%' + feature + '%',))
    results = cursor.fetchall()
    return results

def display_results(results):
    """Clear the table and display search results."""
    for row in tree.get_children():
        tree.delete(row)
    for row in results:
        tree.insert("", tk.END, values=row)

def on_search():
    """Handle search button click."""
    feature = entry_feature.get()
    if not feature:
        messagebox.showerror("Input Error", "Please enter a feature to search.")
        return
    results = search_units_by_feature(feature)
    if results:
        display_results(results)
    else:
        messagebox.showinfo("No Results", "No rental units found with the specified feature.")



#Fucntion to go back to phase2gui
def back_btn():
    root.destroy()
    subprocess.Popen(["python3", "phase2gui.py"])  #Reopen the add unit window




# GUI setup
root = tk.Tk()
root.title("Rental Unit Feature Search")
root.geometry("900x700")

# Feature input and search button
tk.Label(root, text="Feature:").grid(row=0, column=0, padx=10, pady=10)
entry_feature = tk.Entry(root)
entry_feature.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Search", command=on_search).grid(row=0, column=2, padx=10, pady=10)



# Back button
tk.Button(root, text="Back", command=back_btn).grid(row=2, column=1, pady=20)


# Results table
columns = ("Title", "Description", "Features", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

# End database connection
conn.close()
