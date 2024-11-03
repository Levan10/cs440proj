from MainDataBase import conn, cursor
from datetime import datetime

def insert_unit(username, title, description, features, price):
    today = datetime.now().strftime('%Y-%m-%d')

    # Check post limits
    cursor.execute('SELECT COUNT(*) FROM rental_units WHERE username = ? AND date_posted = ?', (username, today))
    daily_post_count = cursor.fetchone()[0]

    if daily_post_count < 2:
        cursor.execute('''
            INSERT INTO rental_units (title, description, features, price, username, date_posted) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, features, price, username, today))
        conn.commit()
        return "Rental unit added successfully."
    else:
        return "Daily post limit reached."
