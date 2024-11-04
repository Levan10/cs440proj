import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sys

# Connect to the SQLite database
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

# Get unit_id, unit_title, and username from command-line arguments or other sources
unit_id = sys.argv[1]
unit_title = sys.argv[2]
username = sys.argv[3]

# Add date_posted column if it doesn't exist
#I had to duplicate the date posted section, it fixes date_posted doesnt exist, will have to full fix later
try:
    cursor.execute("ALTER TABLE reviews ADD COLUMN date_posted TEXT")
    conn.commit()
except sqlite3.OperationalError:
    # Column already exists
    pass

# Function to submit a review
def submit_review():
    rating = rating_var.get()
    description = entry_description.get("1.0", tk.END).strip()

    # Get today's date formatted as YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')  # Current date

    if not rating or not description:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    # Check if the user is the owner of the rental unit
    cursor.execute("SELECT username FROM rental_units WHERE unit_id = ?", (unit_id,))
    unit_owner = cursor.fetchone()
    if unit_owner and unit_owner[0] == username:
        messagebox.showerror("Review Error", "You cannot review your own rental unit.")
        return

    # Check how many reviews the user has submitted today
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE username = ? AND date_posted = ?", (username, today))
    review_count = cursor.fetchone()[0]
    if review_count >= 3:
        messagebox.showerror("Review Limit", "You can only submit 3 reviews per day.")
        return

    # Check if the user has already reviewed this rental unit
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE username = ? AND unit_id = ?", (username, unit_id))
    has_reviewed = cursor.fetchone()[0]
    if has_reviewed > 0:
        messagebox.showerror("Review Error", "You have already reviewed this rental unit.")
        return

    # Insert the new review into the database
    cursor.execute("""
        INSERT INTO reviews (unit_id, username, rating, description, date_posted)
        VALUES (?, ?, ?, ?, ?)
    """, (unit_id, username, rating, description, today))

    conn.commit()
    messagebox.showinfo("Success", "Your review has been submitted successfully.")
    root.destroy()


# GUI setup
root = tk.Tk()
root.title("Submit Review for " + unit_title)

tk.Label(root, text="Username: " + username).pack(pady=10)
tk.Label(root, text="Rental Unit: " + unit_title).pack(pady=10)

tk.Label(root, text="Rating:").pack(pady=10)
rating_var = tk.StringVar(value="")
rating_options = tk.OptionMenu(root, rating_var, "excellent", "good", "fair", "poor")
rating_options.pack(pady=5)

tk.Label(root, text="Description:").pack(pady=10)
entry_description = tk.Text(root, height=5, width=40)
entry_description.pack(pady=5)

tk.Button(root, text="Submit Review", command=submit_review).pack(pady=20)

def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
