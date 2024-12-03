import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys

# Database Connection
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

def search_units_by_feature(feature):
    cursor.execute("""
        SELECT unit_id, title, description, features, price
        FROM rental_units
        WHERE features LIKE ?
        ORDER BY price DESC
    """, ('%' + feature + '%',))
    return cursor.fetchall()

def find_users_with_two_units(feature1, feature2):
    cursor.execute("""
        SELECT DISTINCT r1.username
        FROM rental_units r1
        JOIN rental_units r2
        ON r1.username = r2.username
        AND r1.date_posted = r2.date_posted
        WHERE r1.features LIKE ? AND r2.features LIKE ?
        AND r1.unit_id != r2.unit_id
    """, ('%' + feature1 + '%', '%' + feature2 + '%'))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_units_with_positive_reviews(user_x):
    cursor.execute("""
        SELECT DISTINCT r.unit_id, r.title, r.description, r.features, r.price
        FROM rental_units r
        JOIN reviews rv ON r.unit_id = rv.unit_id
        WHERE r.username = ?
        AND rv.rating IN ('excellent', 'good')
        AND NOT EXISTS (
            SELECT 1
            FROM reviews rv2
            WHERE rv2.unit_id = r.unit_id AND rv2.rating NOT IN ('excellent', 'good')
        )
    """, (user_x,))
    return cursor.fetchall()

def get_top_users_by_date(target_date):
    cursor.execute("""
        SELECT r.username, COUNT(*) as post_count
        FROM rental_units r
        WHERE r.date_posted = ?
        GROUP BY r.username
        HAVING COUNT(*) = (
            SELECT MAX(post_count)
            FROM (
                SELECT username, COUNT(*) as post_count
                FROM rental_units
                WHERE date_posted = ?
                GROUP BY username
            )
        )
    """, (target_date, target_date))
    return cursor.fetchall()

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

def on_find_users():
    feature1 = entry_feature1.get()
    feature2 = entry_feature2.get()
    if not feature1 or not feature2:
        messagebox.showerror("Input Error", "Please enter both features.")
        return
    results = find_users_with_two_units(feature1, feature2)
    user_results_box.delete("1.0", tk.END)
    if results:
        user_results_box.insert(tk.END, "\n".join(results))
    else:
        user_results_box.insert(tk.END, "No users found matching the criteria.")

def on_get_units_with_positive_reviews():
    selected_user = dropdown_user.get()
    if not selected_user:
        messagebox.showerror("Input Error", "Please select a user.")
        return
    results = get_units_with_positive_reviews(selected_user)
    if results:
        display_results(results)
    else:
        messagebox.showinfo("No Results", "No rental units found with only positive reviews.")

def on_get_top_users_by_date():
    selected_date = dropdown_date.get()
    if not selected_date:
        messagebox.showerror("Input Error", "Please select a date.")
        return
    results = get_top_users_by_date(selected_date)
    if results:
        top_users = "\n".join([f"{row[0]}: {row[1]} posts" for row in results])
        messagebox.showinfo("Top Users", f"Users with the most posts on {selected_date}:\n{top_users}")
    else:
        messagebox.showinfo("No Results", f"No users found with posts on {selected_date}.")

def open_review_interface(username):
    selected_item = tree.focus()  # Get the selected item in the Treeview
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a rental unit to review.")
        return

    selected_values = tree.item(selected_item, 'values')
    unit_id = selected_values[0]
    unit_title = selected_values[1]

    # Pass the username, unit_id, and title to the review interface
    subprocess.Popen(["python3", "phase2review.py", str(unit_id), unit_title, username])

# GUI setup
root = tk.Tk()
root.title("Rental Unit Feature Search")
root.geometry("1000x800")

# Feature input and search button
tk.Label(root, text="Feature:").grid(row=0, column=0, padx=10, pady=10)
entry_feature = tk.Entry(root)
entry_feature.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Search", command=on_search).grid(row=0, column=2, padx=10, pady=10)

# Two text fields for user criteria search
tk.Label(root, text="Feature 1:").grid(row=2, column=0, padx=10, pady=10)
entry_feature1 = tk.Entry(root)
entry_feature1.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Feature 2:").grid(row=3, column=0, padx=10, pady=10)
entry_feature2 = tk.Entry(root)
entry_feature2.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Find Users", command=on_find_users).grid(row=4, column=0, columnspan=2, pady=10)

# Label for text box
tk.Label(root, text="Users with two units matching the criteria:", font=("Arial", 14, "bold")).grid(row=5, column=0, columnspan=3, pady=5)

# Text box for displaying users
user_results_box = tk.Text(root, height=10, width=60, bg="lightyellow", fg="black", font="12", wrap=tk.WORD)
user_results_box.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Dropdown for user selection (for units with positive reviews)
cursor.execute("SELECT username FROM users")
users = [row[0] for row in cursor.fetchall()]

tk.Label(root, text="Select User:").grid(row=7, column=0, padx=10, pady=10)
dropdown_user = ttk.Combobox(root, values=users)
dropdown_user.grid(row=7, column=1, padx=10, pady=10)

# Button for positive reviews functionality
tk.Button(root, text="Get Units with Positive Reviews", command=on_get_units_with_positive_reviews).grid(row=8, column=0, columnspan=2, pady=10)

# Dropdown for selecting a date (for top users by date)
cursor.execute("SELECT DISTINCT date_posted FROM rental_units")
dates = [row[0] for row in cursor.fetchall()]

tk.Label(root, text="Select Date:").grid(row=10, column=0, padx=10, pady=10)
dropdown_date = ttk.Combobox(root, values=dates)
dropdown_date.grid(row=10, column=1, padx=10, pady=10)

# Button for "Find Users by Date" functionality
tk.Button(root, text="Get Top Users by Date", command=on_get_top_users_by_date).grid(row=11, column=0, columnspan=2, pady=10)

# Get the logged-in username from command-line arguments
if len(sys.argv) > 1:
    logged_in_user = sys.argv[1]  # This will be the username of the logged-in user
else:
    logged_in_user = None  # Handle case where no username is passed

# Review button using the logged-in username
review_button = tk.Button(root, text="Review", command=lambda: open_review_interface(logged_in_user))
review_button.grid(row=0, column=3, padx=10, pady=10)

# Results table with Unit ID column
columns = ("Unit ID", "Title", "Description", "Features", "Price")
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
