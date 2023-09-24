def setup_mysql_db(cursor, database, personnel_table_name, attendance_table_name, mysql_unknown_name_table):
    
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
    CREATE TABLE IF NOT EXISTS {attendance_table_name} (
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
    CREATE TABLE IF NOT EXISTS {personnel_table_name} (
        student_id INT NOT NULL,
        university VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL
    );
    ''')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {mysql_unknown_name_table} (
        person_id INT NOT NULL,
        date DATE NULL,
        in_time TIME NULL
    );
    ''')