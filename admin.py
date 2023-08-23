import face_recognition


class Admin:

    def __init__(self):
        pass

    def image_to_encoding(self, image):
        encoding= face_recognition.face_encodings(image)[0]
        return encoding
    

    def make_entry(self, student_id: int, student_name:str, batch:str, method='cam'):
        if method == 'cam':
            pass
            
        elif method == 'img':
            pass
            

    def make_entry_from_image(self,student_id: int, student_name:str, batch:str,path):
        face=face_recognition.load_image_file(path)
        image_encoding = self.image_to_encoding(face)





    
            
            
    