import json
import mysql.connector

def parse_config_file(path='../config.json'):

    with open(path, 'r') as config_file:
        config_data = json.load(config_file)

    server = config_data['server']
    username = config_data['username']
    password = config_data['password']
    database = config_data['database']
    personnel_table_name = config_data['personnel_table_name']
    attendance_table_name = config_data['attendance_table_name']
    mysql_unknown_name_table = config_data['mysql_unknown_name_table']

    return server, username, password, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table

def connect_mysql_database(server: str, username: str, password : str) -> tuple :
    '''Connects to a MySQL server and sets the table names for 3 required tables'''
    try:
        config = {
            "host": server,
            "user": username,
            "password": password
        }

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        return connection, cursor
    
    except:
        print("Couldn't connect to MySQL database server! Please check your credentials.")
        exit()

server, username, password, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table = parse_config_file(path='../config.json')

connection, cursor = connect_mysql_database(server, username, password)

# Creating schema (database)
cursor.execute(f"""
CREATE DATABASE IF NOT EXISTS {database};
""")

# Using the created databse
cursor.execute(f"""
USE {database};
""")

# Creating attendance table
cursor.execute(f'''
CREATE TABLE {attendance_table_name} (
    student_id INT NOT NULL,
    university VARCHAR(255) NOT NULL,
    date DATE NULL,
    attendance BOOLEAN NULL,
    in_time TIME NULL,
    entry_exit TEXT NULL
);
''')

# Creating personnel table
cursor.execute(f'''
CREATE TABLE {personnel_table_name} (
    student_id INT NOT NULL,
    university VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);
''')

cursor.execute(f'''
CREATE TABLE {mysql_unknown_name_table} (
    person_id INT NOT NULL,
    date DATE NULL,
    in_time TIME NULL
);
''')

cursor.close()
connection.close()
