import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    user='ordynator',
    password='root'
)

cursor = conn.cursor()


with open('create_psychiatric_hospital.sql', 'r') as file:
    sql_script = file.read()


for statement in sql_script.split(';'):
    if statement.strip():
        cursor.execute(statement)


conn.commit()
cursor.close()
conn.close()

