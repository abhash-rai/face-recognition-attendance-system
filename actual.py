import face_recognition
import cv2
import numpy as np
import os


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

    def __init__(self, scale_frame=0.5, face_location_model='hog', face_encoding_model = 'small'):

        def retrieve_faces_encodings():
            '''Retrieves and retuns dictionary (key is face enoding and value is the student id) of faces encoding from the server'''
            return { tuple(np.load('./database/face_encodings/'+encoded_face_id)):encoded_face_id.split('.')[0] for encoded_face_id in os.listdir('./database/face_encodings/') }

        self.__encodings_database = retrieve_faces_encodings()
        self.__encodings_database_encodings_only = [np.array(tuple_representation) for tuple_representation in self.__encodings_database.keys() ] # Getting faces encodings only from the database

        self.__identified_student_ids = []
        self.scale_frame = scale_frame

        self.process_current_frame = True
        self.face_location_model = face_location_model #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.face_encoding_model = face_encoding_model #'large' model has better accuracy but is slower, 'small' model is faster

    def send_identified_ids_to_server(student_ids: list) -> None:
        '''Sends the given list of student ids to the server'''
        pass

    def image_array_to_face_encoding(image_numpy_arr: np.array) -> np.array:
        '''Inputs numpy array representation of an image and returns the 122 dimentional (numpy) encoding of every faces in the picture in a list'''
        return face_recognition.face_encodings(image_numpy_arr)
    
    def start_session(self, show_preview=True, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
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

            print(self.__identified_student_ids)
            self.send_identified_ids_to_server() # Call function to send identified student ids to the server for attendance

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
                
                if cv2.waitKey(1) & 0xFF == ord('q'): # Break the loop if 'q' key is pressed
                    break

            self.__identified_student_ids = [] #Reset the variable

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

Session = Attendance()
Session.start_session(show_preview=False)