import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import sys

# Connect to the Rental_Units database
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

# Retrieve the title of the rental unit passed as an argument when opening this window
rental_title = sys.argv[1] if len(sys.argv) > 1 else ""

# Function to submit the review to the database
def submit_review():
    # Get user inputs
    username = entry_username.get()
    rating = rating_var.get()
    description = entry_description.get("1.0", tk.END).strip()

    # Validation to ensure fields are filled
    if not username or not rating or not description:
        messagebox.showerror("Input Error", "Please fill out all fields.")
        return

    # Find the unit ID based on the title (assuming titles are unique)
    cursor.execute("SELECT unit_id FROM rental_units WHERE title = ?", (rental_title,))
    unit_id_row = cursor.fetchone()
    if unit_id_row is None:
        messagebox.showerror("Error", "Selected rental unit not found.")
        return
    unit_id = unit_id_row[0]

    # Check that the user hasn't already reviewed this unit
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE unit_id = ? AND username = ?", (unit_id, username))
    if cursor.fetchone()[0] > 0:
        messagebox.showerror("Duplicate Review", "You have already reviewed this rental unit.")
        return

    # Insert the review into the database
    cursor.execute('''
        INSERT INTO reviews (unit_id, username, rating, description, date_posted)
        VALUES (?, ?, ?, ?, date('now'))
    ''', (unit_id, username, rating, description))
    conn.commit()
    messagebox.showinfo("Success", "Review submitted successfully.")
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Submit Review")
root.geometry("600x400")

# Display the rental title
tk.Label(root, text=f"Review for: {rental_title}", font=("Arial", 14)).pack(pady=10)

# Username entry
tk.Label(root, text="Username").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

# Rating dropdown menu
tk.Label(root, text="Rating").pack(pady=5)
rating_var = tk.StringVar()
rating_dropdown = ttk.Combobox(root, textvariable=rating_var, values=["Excellent", "Good", "Fair", "Poor"])
rating_dropdown.pack()

# Description text area
tk.Label(root, text="Description").pack(pady=5)
entry_description = tk.Text(root, height=5, width=50)
entry_description.pack()

# Submit button
tk.Button(root, text="Submit Review", command=submit_review).pack(pady=20)

# Close database connection on window close
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
