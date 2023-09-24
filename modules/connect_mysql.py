import mysql.connector

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
