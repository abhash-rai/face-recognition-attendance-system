import face_recognition
import cv2
import numpy as np
import pandas as pd
import ast

# class Admin:

#     def __init__(self):
#         self.__db_path = './database/students.csv'

#     def add_entry_to_db(self, encoding, student_id: int, student_name:str, batch:str):
#         encoding = str(list(encoding))
#         df = pd.read_csv(self.__db_path)
#         print(df)
#         df.loc[len(df)] = [encoding, student_id, student_name, batch]
#         print(df)
#         df.to_csv(self.__db_path, index=False)

#     def image_to_encoding(self, image):
#         encoding= face_recognition.face_encodings(image)
#         return encoding
    
#     def capture_frame(cam_index=0):
#         cap = cv2.VideoCapture(0)
#         if not cap.isOpened():
#             print("Error: Could not open camera.")
#             return
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Could not capture a frame.")
#             cap.release()
#             return
#         captured_image_array = np.array(frame)
#         cap.release()
#         return captured_image_array

#     def make_entry_from_cam(self, student_id: int, student_name:str, batch:str, cam_index=0):
#         captured = self.capture_frame
#         face_encoding = self.image_to_encoding(captured)[0]
#         self.add_entry_to_db(face_encoding, student_id, student_name, batch)
            

#     def make_entry_from_image(self,student_id: int, student_name:str, batch:str,path):
#         face=face_recognition.load_image_file(path)
#         image_encoding = self.image_to_encoding(face)[0]
#         self.add_entry_to_db(image_encoding, student_id, student_name, batch)

# a = Admin()

# b = a.make_entry_from_cam(1,'Abhash', 'BCU',)






class Admin:

    def __init__(self):
        self.__db_path = './database/students.csv'
        self.__db_encoded_faces = [ np.array(ast.literal_eval(encoded_data)) for encoded_data in pd.read_csv(self.__db_path)['encoding'] ]
        self.__process_current_frame = True

    def add_entry_to_db(self, encoding, student_id: int, first_name:str, middle_name:str, last_name:str, semester:int, course: str, university: str) -> None:
        encoding = str(list(encoding))
        df = pd.read_csv(self.__db_path)
        df.loc[len(df)] = [encoding, student_id, first_name, middle_name, last_name, semester, course, university]
        df.to_csv(self.__db_path, index=False)

    def image_to_encoding(self, image):
        encoding= face_recognition.face_encodings(image)
        return encoding

    def make_entry_from_image(self, student_id: int, first_name:str, middle_name:str, last_name:str, semester:int, course: str, university: str, path:str):
        image=face_recognition.load_image_file(path)
        image_encoding = self.image_to_encoding(image)
        if len(image_encoding) > 1:
            print('Please provide an image with a single face for entry!')
            return
        elif len(image_encoding) == 0:
            print('Please provide an image with atleast a visibly clear single face for entry!')
            return
        else:
            self.add_entry_to_db(image_encoding[0], student_id, first_name, middle_name, last_name, semester, course, university)

admin = Admin()
admin.make_entry_from_image(
    student_id = 1,
    first_name = 'Abhash', 
    middle_name = '', 
    last_name = 'Rai', 
    semester = 3, 
    course = 'Bsc (Hons) Computer and Data Science', 
    university = 'BCU', 
    path = './images/imgs/Sudeep.jpg'
)