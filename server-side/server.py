import face_recognition
import pandas as pd
import numpy as np
import os 
import ast

from fastapi import FastAPI
from typing import Dict


students_csv_path = './database/students.csv'
students_csv = pd.read_csv(students_csv_path)

attendance_csv_path = './database/attendance.csv'
attendance_csv = pd.read_csv(attendance_csv_path).set_index('unique_identifier')

face_endcodings_directory_path = './database/face_encodings/'
known_face_encodings_id_dict = { tuple(np.load(face_endcodings_directory_path+encoded_face_id)):encoded_face_id.split('.')[0] for encoded_face_id in os.listdir(face_endcodings_directory_path) }
known_face_encodings_only = list(known_face_encodings_id_dict.keys())

def make_attendance(student_encondings_time_dict: dict) -> None:
    '''Iterates over the given dict items and makes attendance'''

    for face_encoding, time in student_encondings_time_dict.items():
        face_encoding = np.array(face_encoding)
        unique_identifier = None
        matches = face_recognition.compare_faces(known_face_encodings_only, face_encoding) # Compare the face encoding with the list of known encoded faces
        if True in matches:
            match_index = matches.index(True)
            matched_encoding = known_face_encodings_only[match_index]
            unique_identifier = known_face_encodings_id_dict[matched_encoding]
        
        if unique_identifier != None:
            if attendance_csv.loc[unique_identifier,'attendance'] == False:
                attendance_csv.loc[unique_identifier,'time'] = time
                attendance_csv.loc[unique_identifier,'attendance'] = True
        attendance_csv.to_csv(attendance_csv_path, index=True) # Saving the new data


app = FastAPI()

@app.post("/recieve-face-encodings/")
async def receive_dict(data: Dict[str, str]):
    """
    This endpoint receives a dictionary from the client and stores it in the data_store.
    """
    data = {ast.literal_eval(key): val for key, val in data.items()}
    make_attendance(data) # Making attendance