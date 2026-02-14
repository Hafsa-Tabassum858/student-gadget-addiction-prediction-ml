import sqlite3
import json

conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

# Ensure the table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        subject TEXT,
        message TEXT
    )
""")

# Now safely select the data
cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

# Save data to JSON
data = [{"id": row[0], "name": row[1], "email": row[2], "subject": row[3], "message": row[4]} for row in rows]

with open("messages_log.json", "w") as file:
    json.dump(data, file, indent=4)

conn.close()
print("Data saved to messages_log.json")
import sqlite3
import json

conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

# Ensure the table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        subject TEXT,
        message TEXT
    )
""")

# Now safely select the data
cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

# Save data to JSON
data = [{"id": row[0], "name": row[1], "email": row[2], "subject": row[3], "message": row[4]} for row in rows]

with open("messages_log.json", "w") as file:
    json.dump(data, file, indent=4)

conn.close()
print("Data saved to messages_log.json")
