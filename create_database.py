import mysql.connector

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='ordynator',
    password='root'
)

cursor = conn.cursor()

# Read the SQL script from a file
with open('create_psychiatric_hospital.sql', 'r') as file:
    sql_script = file.read()

# Execute the script
for statement in sql_script.split(';'):
    if statement.strip():
        cursor.execute(statement)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

