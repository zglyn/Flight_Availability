import sqlite3

# Create flights.db 
conn = sqlite3.connect('flights.db')
cursor = conn.cursor()

# Read the flights.sql file
with open('flights.sql', 'r') as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print("'flights.db' successfully created using flights.sql")