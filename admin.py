import face_recognition
import cv2
import numpy as np
import pandas as pd

class Admin:

    def __init__(self):
        self.__db_path = './database/students.csv'

    def add_entry_to_db(self, encoding, student_id: int, student_name:str, batch:str):
        new_entry = {
            'encoding': encoding,
            'student_id': student_id,
            'student_name': student_name,
            'batch': batch
        }
        df = pd.read_csv(self.__db_path)
        df.loc[len(df)] = new_entry
        df.to_csv(self.__db_path, index=False)

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
        face_encoding = self.image_to_encoding(captured)[0]
        self.add_entry_to_db(face_encoding, student_id, student_name, batch)
            

    def make_entry_from_image(self,student_id: int, student_name:str, batch:str,path):
        face=face_recognition.load_image_file(path)
        image_encoding = self.image_to_encoding(face)[0]





    
            
            
    