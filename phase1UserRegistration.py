from MainDataBase import conn, cursor, hash_password, check_password
import sqlite3

# Function for registering a new user
def signup(username, password, confirm_password, first_name, last_name, email, phone):
    if password != confirm_password:
        return "Passwords do not match."

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password, firstName, lastName, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
            (username, hashed_password, first_name, last_name, email, phone))
        conn.commit()
        return "User registered successfully."
    except sqlite3.IntegrityError:
        return "Username or email already exists."


# Function for logging in a user
def login(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and check_password(result[0], password):
        return "Login successful!"
    return "Invalid username or password."

