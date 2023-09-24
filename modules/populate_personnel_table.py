import mysql.connector
import os
import pickle

def make_personnel_entry(pickle_encodings_path, connection, cursor, database_name, personnel_table_name):
    try:
        if os.path.exists(pickle_encodings_path):

            with open(pickle_encodings_path, "rb") as file:
                loaded_data = pickle.load(file)

                # Using given databse
                cursor.execute(f"""
                USE {database_name};
                """)

                for key in loaded_data.keys():
                    id, university, first_name, last_name = key.split("-")

                    # Use placeholders to prevent SQL injection
                    query = f"SELECT * FROM {personnel_table_name} WHERE student_id = %s"
                    cursor.execute(query, (id,))
                    existing_data = cursor.fetchone()

                    if existing_data:
                        print(f"Data with ID {id} already exists. Skipping insertion.")
                    else:
                        # Use placeholders to prevent SQL injection
                        insert_query = f"INSERT INTO {personnel_table_name} (student_id, university, first_name, last_name) VALUES (%s, %s, %s, %s)"
                        values = (id, university, first_name, last_name)
                        cursor.execute(insert_query, values)

            connection.commit()
            print("Data inserted successfully.")

        else:
            print("No encodings found. Please run validateData_generator for generating encoding first")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
