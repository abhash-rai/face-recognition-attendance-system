import face_recognition
import cv2
import numpy as np

class Admin:

    def __init__(self):
        pass

    def image_to_encoding(self, image):
        encoding= face_recognition.face_encodings(image)[0]
        return encoding
    
    def capture_frame(cam_index=0):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture a frame.")
            cap.release()
            return
        captured_image_array = np.array(frame)
        cap.release()
        return captured_image_array

    def make_entry_from_cam(self, student_id: int, student_name:str, batch:str, cam_index=0):
        captured = self.capture_frame
        face_encoding = self.image_to_encoding(captured)
            
    