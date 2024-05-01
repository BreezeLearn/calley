import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()

# Add a new column named 'new_column' to the 'your_table' table
cursor.execute('''ALTER TABLE bots
                  ADD COLUMN user_id TEXT''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()
