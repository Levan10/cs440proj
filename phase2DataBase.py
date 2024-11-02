import sqlite3
from datetime import datetime

# In phase2DataBase(this) file, creating simple tables required for the user.
# In the req, user can have the ability to enter a rental unit, view the rental units, and review them.
# A user cannot review their own unit and is limited to 2 posts per day and 3 reviews per day
# (Gonna have to figure out the time system)
# Review consists of, "A dropdown menu to choose "excellent/good/fair/poor", and then a description such as
# "This is a cool place to rent."

conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

# Create tables for users, rental units, and reviews
def create_tables():
    # User table to track registered users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')

    # Rental units table, with an autoincremented ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rental_units (
            date_posted TEXT,
            unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            features TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')

    # Reviews table, tracking reviews with constraints
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            date_posted TEXT,
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_id INTEGER,
            username TEXT NOT NULL,
            rating TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (unit_id) REFERENCES rental_units(unit_id),
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')

    conn.commit()

def close_connection():
    conn.close()
