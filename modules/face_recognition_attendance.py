import mysql.connector
import cv2
import pickle
import datetime
import face_recognition

class Session:




    def __init__(self, face_encodings_path, unknwon_face_store_location, face_location_model='hog', face_encoding_model = 'small', time_between_entry_exit=300):

        self.__face_encodings_pkl_path = face_encodings_path
        self.unknwon_face_store_location = unknwon_face_store_location
        
        self.face_location_model = face_location_model #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.face_encoding_model = face_encoding_model #'large' model has better accuracy but is slower, 'small' model is faster

        with open(self.__face_encodings_pkl_path, 'rb') as file:
            self.__known_face_encodings = pickle.load(file)

        self.__connection = None
        self.__cursor = None

        self.__mysql_personnel_table = None
        self.__mysql_attendance_table = None
        self.__mysql_unknown_table = None

        self.__time_between_entries = time_between_entry_exit # in seconds

        self.__not_identified_face_encodings = []







    def get_current_date(self) -> str:
        """
        Get the current date and returns a string representing the current date in the format 'YYYY-MM-DD'.
        """
        current_date = datetime.date.today()
        return str(current_date)
    






    def get_current_time(self) -> str:
        '''Gets the current timestamp with seconds precision, converts it to string, and returns it'''
        return datetime.datetime.now().strftime('%H:%M:%S')
    






    def connect_mysql_database(self, server: str, username: str, password : str, database: str, personnel_table_name: str, attendance_table_name: str, mysql_unknown_name_table: str) -> tuple :
        '''Connects to a MySQL server and sets the table names for 3 required tables'''
        try:
            config = {
                "host": server,
                "user": username,
                "password": password,
                "database": database
            }

            self.__connection = mysql.connector.connect(**config)
            self.__cursor = self.__connection.cursor()
            
            self.__mysql_personnel_table = personnel_table_name
            self.__mysql_attendance_table = attendance_table_name
            self.__mysql_unknown_table = mysql_unknown_name_table
        
        except:
            print("Couldn't connect to MySQL database server! Please check your credentials.")
            exit()







    def initialize_attendance_today(self):
        '''Initializes attendance for the current date (only if it is not already initialized) with every individual as absent by default'''

        self.__cursor.execute(f"SELECT MAX(date) FROM {self.__mysql_attendance_table};")
        latest_date = self.__cursor.fetchone()[0]

        if latest_date is None or latest_date != datetime.date.today():
            self.__cursor.execute(f"SELECT student_id, university FROM {self.__mysql_personnel_table};")
            personnel_data = self.__cursor.fetchall() # Fetch all rows from the "personnel" table

            # Insert data into the "attendance" table
            for row in personnel_data:
                student_id, university = row
                self.__cursor.execute(
                    f"INSERT INTO {self.__mysql_attendance_table} (student_id, university, date, attendance, in_time, entry_exit) VALUES (%s, %s, %s, NULL, NULL, NULL)",
                    (student_id, university, self.get_current_date())
                )

            self.__connection.commit()







    def checking_time_interval(self, time_interval_seconds: int, time_str: str):
        try:
            start_time = datetime.datetime.strptime(time_str, '%H:%M:%S')

            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            current_time = datetime.datetime.strptime(current_time, '%H:%M:%S')

            time_difference = (current_time - start_time).total_seconds() # time interval in seconds

            if time_difference >= time_interval_seconds:
                return True
            else:
                return False

        except ValueError:
            # Handle invalid time strings
            print("Invalid time format. Please use 'HH:MM:SS' format.")
            return None








    def make_known_entry(self, student_id: int, student_university: str, date, time):
        self.__cursor.execute(f"SELECT entry_exit FROM {self.__mysql_attendance_table} WHERE student_id = %s AND university = %s AND date = %s", (int(student_id), student_university, date))
        entry_exit = self.__cursor.fetchone()[0]

        if entry_exit is None:
            self.__cursor.execute("SET SQL_SAFE_UPDATES = 0;")
            self.__cursor.execute(
                f"UPDATE {self.__mysql_attendance_table} SET attendance = 1, in_time = %s, entry_exit = %s WHERE student_id = %s AND university = %s AND date = %s",
                (time, time, student_id, student_university, date)
            )
            self.__cursor.execute("SET SQL_SAFE_UPDATES = 1;")
            self.__connection.commit()
        else:
            last_entry = entry_exit.split(',')[-1]
            
            if self.checking_time_interval(self.__time_between_entries, last_entry): # Only execute if desired time interval in seconds have passed between last entry and now
                entry_exit = entry_exit + f',{time}'
                self.__cursor.execute("SET SQL_SAFE_UPDATES = 0;")
                self.__cursor.execute(
                    f"UPDATE {self.__mysql_attendance_table} SET attendance = 1, entry_exit = %s WHERE student_id = %s AND university = %s AND date = %s",
                    (entry_exit, student_id, student_university, date)
                )
                self.__cursor.execute("SET SQL_SAFE_UPDATES = 1;")
                self.__connection.commit()

    





    def make_unknown_entry(self, encoding, frame, date: str, in_time: str):

        def entry_into_db():
            self.__cursor.execute(f"SELECT MAX(person_id) FROM {self.__mysql_unknown_table};")
            person_count = self.__cursor.fetchone()[0]

            if person_count is None:
                person_count = 1
                self.__cursor.execute(
                    f"INSERT INTO {self.__mysql_unknown_table} (person_id, date, in_time) VALUES (%s, %s, %s)",
                    (person_count, date, in_time)
                )
                self.__connection.commit()
            else:
                person_count += 1
                self.__cursor.execute(
                    f"INSERT INTO {self.__mysql_unknown_table} (person_id, date, in_time) VALUES (%s, %s, %s)",
                    (person_count, date, in_time)
                )
                self.__connection.commit()
            
            return person_count

        if len(self.__not_identified_face_encodings) == 0:
            self.__not_identified_face_encodings.append(encoding)
            
            person_count = entry_into_db()
                    
            cv2.imwrite(f'{self.unknwon_face_store_location}/{person_count}.jpg', frame)
            
        else:
            if True not in face_recognition.api.compare_faces(self.__not_identified_face_encodings, encoding):
                self.__not_identified_face_encodings.append(encoding)
                
                person_count = entry_into_db()
                    
                cv2.imwrite(f'{self.unknwon_face_store_location}/{person_count}.jpg', frame)







    def compare_faces(self, known: dict, unknown, tolerance):
        for student_identity, face_encoding in known.items():
            if True in face_recognition.api.compare_faces(face_encoding, unknown, tolerance=tolerance):
                return student_identity
        return None
    






    def start_session(self, camera_index=0, show_preview=True, scale_frame=0.77, desired_fps=2, tolerance=0.45):

        try:

            cap = cv2.VideoCapture(camera_index)
            frame_delay = int(1000 / desired_fps)  # Delay in milliseconds between frames based on the desired FPS
            
            while True:
                ret, frame = cap.read()

                small_frame = cv2.resize(frame, (0, 0), fx=scale_frame, fy=scale_frame) # Resize the frame for faster processing
                rgb_frame = small_frame[:, :, ::-1] # Convert the frame from BGR to RGB

                face_locations = face_recognition.face_locations(rgb_frame, model=self.face_location_model) # Find face locations and face encodings in the frame
                unknown_face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) # Generate encodings of every faces in the frame in a list
                number_of_faces_detected = len(unknown_face_encodings)

                self.__identified_student_ids = []

                if number_of_faces_detected != 0: # Send data only if one or more person is detected
                    date = self.get_current_date()
                    time = self.get_current_time()

                    for unknown_face in unknown_face_encodings:
                        id = self.compare_faces(self.__known_face_encodings, unknown_face, tolerance=tolerance)
                        
                        if id is not None:
                            student_id, student_uni, first_name, last_name = id.split('-')

                            # Sending to mysql database
                            self.make_known_entry(
                                student_id = student_id,
                                student_university = student_uni,
                                date = date,
                                time = time
                            )

                        else:
                            id = 'Unknown'

                            self.make_unknown_entry(unknown_face, frame, date, time)  # Sending to mysql database
                        
                        self.__identified_student_ids.append(id)

                if show_preview == True: 

                    # Draw rectangles around detected faces and display names on 'the scaled frame'
                    for (top, right, bottom, left), identity in zip(face_locations, self.__identified_student_ids):
                        cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(small_frame, identity, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                    
                    cv2.imshow('Attendance Session Started', small_frame) # Display the frame with face rectangles
                    
                    if cv2.waitKey(frame_delay) & 0xFF == ord('q'): # Break the loop if 'q' key is pressed
                        break

        except KeyboardInterrupt:
            pass  # Handle keyboard interrupt (e.g., for clean exit)

        finally:
            cap.release()  # Release the camera
            cv2.destroyAllWindows()  # Close OpenCV windows
            self.__connection.close()
            self.__cursor.close()