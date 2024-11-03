import sqlite3
import bcrypt
from datetime import datetime

# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('Rental_Units.db')
cursor = conn.cursor()

# Create tables for users, rental units, and reviews
def create_tables():
    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL
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

# Function to hash the password using bcrypt for security
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify that the provided password matches the stored hashed password
def check_password(hashed_password: bytes, user_password: str) -> bool:
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Close the database connection when done
def close_connection():
    conn.close()

# Call this function to ensure the tables are created when the script is run
if __name__ == "__main__":
    create_tables()
