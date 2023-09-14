import os
import cv2
import pickle
import datetime
import face_recognition

class Session:

    def __init__(self, face_location_model='hog', face_encoding_model = 'small'):

        self.face_location_model = face_location_model #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.face_encoding_model = face_encoding_model #'large' model has better accuracy but is slower, 'small' model is faster

        self.__face_encodings_pkl_path = './database/known_face_encodings'
        with open(self.__face_encodings_pkl_path, 'rb') as file:
            self.__known_face_encodings = pickle.load(file)

    def get_current_time(self) -> str:
        '''Gets the current timestamp with seconds precision, converts it to string, and returns it'''
        return datetime.datetime.now().strftime('%H:%M:%S')

    def compare_faces(self, known: dict, unknown, tolerance=0.6):
        for student_identity, face_encoding in known.items():
            if True in face_recognition.api.compare_faces(face_encoding, unknown, tolerance=tolerance):
                return student_identity
        return None

    def start_session(self, camera_index=0, show_preview=True, scale_frame=0.75, desired_fps=2, tolerance=0.6):
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
                    time = self.get_current_time()
                    print(f'[FACE DETECTION] {number_of_faces_detected} faces detected at {time}')
                    for unknown_face in unknown_face_encodings:
                        id = self.compare_faces(self.__known_face_encodings, unknown_face, tolerance=tolerance)
                        if id is None:
                            id = 'Unknown'
                        self.__identified_student_ids.append(id)

                if show_preview == True: 
                    # Draw rectangles around detected faces and display names on 'the scaled frame'
                    for (top, right, bottom, left), identity in zip(face_locations, self.__identified_student_ids):
                        cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(small_frame, identity, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                    
                    cv2.imshow('Face Detection (Scaled Frames)', small_frame) # Display the frame with face rectangles
                    
                    if cv2.waitKey(frame_delay) & 0xFF == ord('q'): # Break the loop if 'q' key is pressed
                        break

        except KeyboardInterrupt:
            pass  # Handle keyboard interrupt (e.g., for clean exit)

        finally:
            cap.release()  # Release the camera
            cv2.destroyAllWindows()  # Close OpenCV windows

a = Session()
a.start_session()