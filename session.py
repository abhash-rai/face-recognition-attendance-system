import face_recognition
import cv2
import datetime
import requests

'''
During execution, this script constantly sends face encodings of detected faces to the server for attendance 
(Logics like if comparing the detected face encodings against face encodings stored in the databse, 
if particular student attendance is already made, making attendence for student whose attendance is not made present
for a particular day is done by the server).

Student Face Encodings is returned to the server in a list of dictionaries.
    * Key should be string of tuple of 122 dimentional face encoding converted from its orignal form of numpy array to use it as dict key
    * Value should be string of the time at which particular face was detected; in the following format:
        [
            { <face1_encoding>: <timestamp1> },
            { <face2_encoding>: <timestamp2> },
            { <face3_encoding>: <timestamp3> }
        ]
        For example: 23140736-BCU
'''


class Attendance:

    def __init__(self, POST_URL: str, scale_frame=0.5, face_location_model='hog', face_encoding_model = 'small'):

        print('\n[START] Session Started.....\n')
        
        self.scale_frame = scale_frame

        self.face_location_model = face_location_model #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.face_encoding_model = face_encoding_model #'large' model has better accuracy but is slower, 'small' model is faster

        self.__POST_URL = POST_URL

    def send_encodings_data(self, json):
        # Send a POST request with the dictionary
        response = requests.post(self.__POST_URL, json=json)

        # Check the response
        if response.status_code == 200:
            print("[SENT] Encodings sent.\n")
            pass
        else:
            print(f"[ERROR] Error sending dictionary: {response.status_code}\n")
            print(response.text)
            
    def get_current_time(self) -> str:
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
            
            number_of_faces_detected = len(face_encodings)
            if number_of_faces_detected != 0: # Send data only if one or more person is detected
                time = self.get_current_time()
                print(f'[FACE DETECTION] {number_of_faces_detected} faces detected at {time}.')
                self.__student_encondings_time_dict = {str(tuple(face_encoding)): time for face_encoding in face_encodings} # This data will be sent to the server for attendance
                self.send_encodings_data(self.__student_encondings_time_dict)
                
            self.__identified_student_ids = [f'Person {n}' for n in range(1, number_of_faces_detected+1)]  
            
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
                
        cap.release() # Release the camera
        cv2.destroyAllWindows() # Close the window
        quit()

if __name__ == '__main__':
    session = Attendance(POST_URL="http://localhost:8000/recieve-face-encodings/")
    session.start_session(show_preview=True)