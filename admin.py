import face_recognition


class Admin:

    def __init__(self):
        pass

    def image_to_encoding(self, image):
        face=face_recognition.load_image_file(image)
        encoding= face_recognition.face_encodings(face)[0]
        return encoding
    

    def make_entry(self, student_id: int, student_name:str, batch:str, method='cam'):
        if method == 'cam':
            pass
            
        elif method == 'img':
            pass
            
    