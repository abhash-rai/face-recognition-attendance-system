import mysql.connector
import os
import pickle

def make_student_entry(file_path = '../database/known_face_encodings'):
    config = {
        "host": "65.109.153.186",
        "user": "sunwayst_Sudeep",
        "password": "iamhello#123",
        "database": "sunwayst_sudeepFullel_bcu"
    }

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                loaded_data = pickle.load(file)
                for key in loaded_data.keys():
                    id, university, first_name, last_name = key.split("-")
                    # Use placeholders to prevent SQL injection
                    query = "SELECT * FROM personnel WHERE student_id = %s"
                    cursor.execute(query, (id,))
                    existing_data = cursor.fetchone()

                    if existing_data:
                        print(f"Data with ID {id} already exists. Skipping insertion.")
                    else:
                        # Use placeholders to prevent SQL injection
                        insert_query = "INSERT INTO personnel (student_id, university, first_name, last_name) VALUES (%s, %s, %s, %s)"
                        values = (id, university, first_name, last_name)
                        cursor.execute(insert_query, values)

            connection.commit()
            print("Data inserted successfully.")

        else:
            print("No encodings found. Please run validateData_generator for generating encoding first")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


make_student_entry()


