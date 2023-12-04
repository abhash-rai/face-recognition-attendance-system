import numpy as np
import cv2
import datetime
import face_recognition

def start_session(encodings_list, enodings_ids, face_location_model, face_encoding_model, camera_index=0, show_preview=True, scale_frame=0.77, desired_fps=5, tolerance=0.44):

    def get_current_date() -> str:
        """
        Get the current date and returns a string representing the current date in the format 'YYYY-MM-DD'.
        """
        current_date = datetime.date.today()
        return str(current_date)
    
    def get_current_time() -> str:
        '''Gets the current timestamp with seconds precision, converts it to string, and returns it'''
        return datetime.datetime.now().strftime('%H:%M:%S')

    enodings_ids = np.array(enodings_ids)

    try:

        cap = cv2.VideoCapture(camera_index)
        frame_delay = int(1000 / desired_fps)  # Delay in milliseconds between frames based on the desired FPS
        
        while True:
            identified_student_ids = []

            ret, frame = cap.read()

            small_frame = cv2.resize(frame, (0, 0), fx=scale_frame, fy=scale_frame) # Resize the frame for faster processing
            rgb_frame = small_frame[:, :, ::-1] # Convert the frame from BGR to RGB

            face_locations = face_recognition.face_locations(rgb_frame, model=face_location_model) # Find face locations and face encodings in the frame
            unknown_face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, model=face_encoding_model) # Generate encodings of every faces in the frame in a list

            if len(unknown_face_encodings) != 0: #Perform operations only if one or more person is detected
                date = get_current_date()
                time = get_current_time()

                for unknown_face in unknown_face_encodings: # For each detected faces, perform facial recognition against known faces

                    identified_id = None

                    status = face_recognition.api.compare_faces(encodings_list, unknown_face, tolerance=tolerance) # Comparing indicidual detected face in a frame against all known faces
                    status = np.array(status)

                    if True in status: # Only if unknown face is recognized

                        recognized_ids_indexes = np.where(status)[0] # Getting list of indexes where the system recoginizes as possible match of the unknown face
                        recognized_ids = enodings_ids[recognized_ids_indexes] # Getting only those ids where the system recoginizes as possible match of the unknown face
                        
                        unique_ids, counts = np.unique(recognized_ids, return_counts=True) # Getting the value counts of the recognized ids (each person will have 3 angles of face encodings: front, left & right)
                        max_number_of_counts = np.max(counts) # Getting the max count

                        if np.count_nonzero(counts == max_number_of_counts) == 1: # Since obtained number is a max count, it should only occur once symbolizing that the system detectes the corresponding it of the max count value is the most confident match of the unknown face
                            max_count_index = np.where(counts == max_number_of_counts)[0][0] # Getting index of the max count value
                            identified_id = unique_ids[max_count_index] # Getting the corresponding ID of the max count value
                            ####### Make known entry to database here

                    else:
                        identified_id = 'Unknown' # If not recognized then the person remains unknown

                        ####### Make unknown entry to database here
                    
                    identified_student_ids.append(identified_id)

            if show_preview == True: 

                # Draw rectangles around detected faces and display names on 'the scaled frame'
                for (top, right, bottom, left), identity in zip(face_locations, identified_student_ids):
                    cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(small_frame, identity, (left, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                
                cv2.imshow('Session', small_frame) # Display the frame with face rectangles
                
                if cv2.waitKey(frame_delay) & 0xFF == ord('q'): # Break the loop if 'q' key is pressed
                    break

    except KeyboardInterrupt:
        pass  # Handle keyboard interrupt (e.g., for clean exit)

    finally:
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close OpenCV windows
        # self.__connection.close()
        # self.__cursor.close()