from phase2DataBase import conn, cursor
from datetime import datetime  # Importing datetime to get the current date


def insert_unit(username, title, description, features, price):
    today = datetime.now().strftime('%Y-%m-%d')  # Get the current date in YYYY-MM-DD format for daily tracking

    # Check if the user exists in the database
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    # If the user does not exist, add them to the users table
    if not user:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()  # Commit the new user addition

    # Check the number of posts the user has made today
    cursor.execute('''SELECT COUNT(*) FROM rental_units WHERE username = ? AND date_posted = ?''',
                   (username, today))  # Query to count today's posts for the user
    daily_post_count = cursor.fetchone()[0]  # Get the result (number of posts today)

    # Enforce the daily limit (only allow 2 posts per user per day)
    if daily_post_count < 2:  # If the user has posted fewer than 2 units today, allow the post
        cursor.execute('''
            INSERT INTO rental_units (title, description, features, price, username, date_posted) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, description, features, price, username, today))  # Insert the new rental unit

        conn.commit()  # Save changes to the database
        return "Rental unit added successfully."

    else:  # If the user has reached the daily limit of 2 posts, deny the post
        return "Daily post limit reached. You can only post 2 rental units per day."
