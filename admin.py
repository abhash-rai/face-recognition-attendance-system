import face_recognition
import cv2
import numpy as np
import pandas as pd
import ast
import sys
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
        self.__student_db = pd.read_csv(self.__db_path)
        self.__db_encoded_faces = [ np.array(ast.literal_eval(encoded_data)) for encoded_data in self.__student_db['encoding'] ]
        self.__process_current_frame = True
        self.__finding_face_location_model = 'hog' #'cnn' has better accuracy but uses GPU, 'hog' is faster with less accuracy uses cpu
        self.__finding_face_encoding_model = 'small' #'large' model has better accuracy but is slower, 'small' model is faster

    def add_entry_to_db(self, encoding, student_id: int, first_name:str, middle_name:str, last_name:str, semester:int, course: str, university: str) -> None:
        encoding = str(list(encoding))
        df = pd.read_csv(self.__db_path)
        df.loc[len(df)] = [encoding, student_id, first_name, middle_name, last_name, semester, course, university]
        df.to_csv(self.__db_path, index=False)

    def image_to_encoding(self, image):
        encoding= face_recognition.face_encodings(image, model = self.__finding_face_encoding_model)
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
    
    def run_recognition(self, preview=False):

        if preview == True:
            video_capture =cv2.VideoCapture(0)

            if not video_capture.isOpened():
                sys.exit("video source not found")

            while True:
                ret, frame = video_capture.read()

                if self.__process_current_frame:
                    small_frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25) # Resized to 50 % of orignal height and width
                    rgb_small_frame= small_frame[:,:,::-1]

                    # find faces
                    self.face_locations = face_recognition.face_locations(rgb_small_frame, model=self.__finding_face_location_model)
                    self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations, model=self.__finding_face_encoding_model)

                    self.students_id = []
                    self.face_names=[]

                    for face_encoding in self.face_encodings:
                        matches = face_recognition.compare_faces(self.__db_encoded_faces, face_encoding)
                        for n, con in enumerate(matches):
                            if con == True:
                                self.face_names.append(f"{self.__student_db.loc[n, 'first_name']} {self.__student_db.loc[n, 'last_name']}")
                            else:
                                self.face_names.append('unknown')


                self.__process_current_frame = not self.__process_current_frame

                # display annotation

                for(top,right,bottom,left), name in zip(self.face_locations,self.face_names):
                    top *=4
                    right *=4
                    bottom *=4
                    left *=4

                    cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255), 2)
                    cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255), -1)
                    cv2.putText(frame, name, (left+6, bottom -6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 1)

                cv2.imshow("Face Recognition", frame)

                if cv2.waitKey(1) == ord("q"):
                    break

            video_capture.release()
            cv2.destroyAllWindows()
        
        else:
            pass

admin = Admin()
# admin.make_entry_from_image(
#     student_id = 1,
#     first_name = 'Abhash', 
#     middle_name = '', 
#     last_name = 'Rai', 
#     semester = 3, 
#     course = 'Bsc (Hons) Computer and Data Science', 
#     university = 'BCU', 
#     path = './images/imgs/Sudeep.jpg'
# )
admin.run_recognition(preview=True)