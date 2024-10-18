from phase1DataBase import conn, cursor, hash_password, check_password
import sqlite3

# Function for registering a new user
def signup(username, password, confirm_password, first_name, last_name, email, phone):
    # Check if the passwords match
    if password != confirm_password:
        return "Passwords do not match!"

    try:
        # Hash the user's password before storing it
        hashed_password = hash_password(password)

        # Insert the new user into the database, while ensuring unique constraints for username, email, and phone
        cursor.execute('''
            INSERT INTO user (username, password, firstName, lastName, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, first_name, last_name, email, phone))
        conn.commit()  # Save changes to the database
        return "User registered successfully!"

    except sqlite3.IntegrityError:
        # Handle duplicate username, email, or phone number
        return "Username, email, or phone already exists!"


# Function for logging in a user
def login(username, password):
    # Retrieve the user's hashed password from the database using the username
    cursor.execute('SELECT password FROM user WHERE username = ?', (username,))
    result = cursor.fetchone()  # Fetch the result of the query

    # Check if the username exists
    if result is None:
        return "User does not exist!"

    # The result is a tuple, so extract the hashed password
    stored_password = result[0]

    # Verify if the provided password matches the stored hashed password
    if check_password(stored_password, password):
        return "Login successful!"
    else:
        return "Incorrect password!"
