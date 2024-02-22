# Creates the database. Only run this once, at first initialization!
# (Add in later if not enough time now, priority task)
import sqlite3

connection = sqlite3.connect('database/database.db')  # Connect the database

with open('database/schema.sql') as f:
    connection.executescript(f.read())  # Open + run schema.sql (Create table)

# FOR TESTING PURPOSES: Create a 'default' profile.
"""cur = connection.cursor()

cur.execute("INSERT INTO character (icon, cname, gender, race, personality, backstory) VALUES (?, ?, ?, ?, ?, ?)",
            ('../static/images/icons/1.png', 'Nox', 'Nonbinary', 'Alien', 'Silly.', 'Spawned in.')
            )

connection.commit()  # Commit changes
connection.close()  # Close it"""