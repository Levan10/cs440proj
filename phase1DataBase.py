import sqlite3
import bcrypt

# Connect to the SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a user table if it doesn't already exist
def create_table():
    (cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        username TEXT PRIMARY KEY,       -- Primary key ensures each username is unique
        password TEXT NOT NULL,          -- Password is required
        firstName TEXT NOT NULL,         -- First name is required
        lastName TEXT NOT NULL,          -- Last name is required
        email TEXT UNIQUE NOT NULL,      -- Email must be unique and not empty
        phone TEXT UNIQUE NOT NULL       -- Phone number must be unique and not empty
    )'''))
    conn.commit()  # Save changes

# Function to hash the password using bcrypt for security
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify that the provided password matches the stored hashed password
def check_password(hashed_password: bytes, user_password: str) -> bool:
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# Close the database connection when done
def close_connection():
    conn.close()
