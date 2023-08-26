import face_recognition
import cv2
import numpy as np
import json
import socket
import ast
import datetime

'''
During execution, this script obtains data from the server once, and constantly sends identified student ids to the 
server for attendance (Logics like if particular student attendance is already made, making attendence for student 
whose attendce is not made for a particular day is done by the server).

Student Face Encodings should be returned to this script in a dictionary format.
    * Key should be tuple of 122 dimentional face encoding converted from its orignal form of numpy array to use it as dict key
    * Value should be string of unique student identification in the following format:
        <student_id>-<university>
        For example: 23140736-BCU
'''


class Attendance:

    def __init__(self, server_ip_address: str, server_port: int, scale_frame=0.5, face_location_model='hog', face_encoding_model = 'small'):
        self.__server_ip_address = server_ip_address
        self.__server_port = server_port

        print('\nSession Started.....\n\nAttempting to recieve session data from the server..\n')

        def retrieve_faces_encodings(server_ip_address: str, server_port: int, chunksize=1024):
            '''Retrieves and retuns dictionary (key is face enoding and value is the student id) of faces encoding from the server'''
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (server_ip_address, server_port)  # the server's IP address and port
            sock.connect(server_address)

            # Receive JSON data
            json_data = b""
            while True:
                chunk = sock.recv(chunksize)
                if not chunk:
                    break
                json_data += chunk

            # Decode and load the received JSON data
            encodings_data = json.loads(json_data.decode())

            while True:
                chunk = sock.recv(chunksize)
                if not chunk:
                    break

            sock.close()
            print("Session data received.")
            face_encodings_json = {ast.literal_eval(key): val for key, val in encodings_data.items()}
            return face_encodings_json

        self.__encodings_database = retrieve_faces_encodings(self.__server_ip_address, self.__server_port)

        self.__encodings_database_encodings_only = [np.array(tuple_representation) for tuple_representation in self.__encodings_database.keys() ] # Getting faces encodings only from the database

        self.__identified_student_ids = []
        self.__identified_student_ids_with_timestamp = {} # This data will be sent to the server for attendance
        self.scale_frame = scale_frame

        self.process_current_frame = True
        self.face_location_model = face_location_model #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.face_encoding_model = face_encoding_model #'large' model has better accuracy but is slower, 'small' model is faster

    def send_identified_ids_timestamps_to_server(self, json: dict, server_ip_address: str, server_port: int, chunksize=1024) -> None:
        '''Sends the given list of student ids to the server'''
        print(json)

    def get_current_time(self):
        '''Gets the current timestamp, converts to string and returns it'''
        return str(datetime.datetime.now().time())
    
    def start_session(self, show_preview=True, camera_index=0, desired_fps=15):
        cap = cv2.VideoCapture(camera_index)
        frame_delay = int(1000 / desired_fps)  # Delay in milliseconds between frames based on the desired FPS
        while True:
            ret, frame = cap.read()

            small_frame = cv2.resize(frame, (0, 0), fx=self.scale_frame, fy=self.scale_frame) # Resize the frame for faster processing
            rgb_frame = small_frame[:, :, ::-1] # Convert the frame from BGR to RGB

            face_locations = face_recognition.face_locations(rgb_frame, model=self.face_location_model) # Find face locations and face encodings in the frame
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) # Generate encodings of every faces in the frame in a list
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.__encodings_database_encodings_only, face_encoding) # Compare the face encoding with the list of known encoded faces
                if True in matches:
                    match_index = matches.index(True)
                    matched_encoding = self.__encodings_database_encodings_only[match_index]
                    identity = self.__encodings_database[tuple(matched_encoding)]
                else:
                    identity = 'Unknown'

                self.__identified_student_ids.append(identity)

                if identity != 'Unknown': # Add the studentid with timestamp only for known students in the database
                    self.__identified_student_ids_with_timestamp[identity] = self.get_current_time()

            self.send_identified_ids_timestamps_to_server(self.__identified_student_ids_with_timestamp, self.__server_ip_address, self.__server_port) # Call function to send identified student ids to the server for attendance

            if show_preview == True: 

                # Draw rectangles around detected faces and display names
                for (top, right, bottom, left), identity in zip(face_locations, self.__identified_student_ids):
                    top *= int(1 / self.scale_frame)
                    right *= int(1 / self.scale_frame)
                    bottom *= int(1 / self.scale_frame)
                    left *= int(1 / self.scale_frame)

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, identity, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                
                cv2.imshow('Face Detection', frame) # Display the frame with face rectangles
                
                if cv2.waitKey(frame_delay) & 0xFF == ord('q'): # Break the loop if 'q' key is pressed
                    break

            self.__identified_student_ids = [] #Reset the variable
            self.__identified_student_ids_with_timestamp = {} #Reset the variable

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

Session = Attendance(server_ip_address='192.168.1.10', server_port=5000)
Session.start_session(show_preview=True)