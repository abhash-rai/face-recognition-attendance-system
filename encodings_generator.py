import os 
import pickle
import face_recognition

def generate_encodings(images_folder_path='./photos'):

    all_face_encodings = {}

    all_directories = os.listdir(images_folder_path)

    for folder in all_directories:
        
        face_encodings = []

        all_files = os.listdir(f'{images_folder_path}/{folder}')
        img_path = [filename for filename in all_files if filename.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp'))] # Filter for image files (e.g., .jpg, .png, .jpeg)
        
        for img in img_path:
            print(f'{images_folder_path}/{folder}/{img}')
            image = face_recognition.api.load_image_file(f'{images_folder_path}/{folder}/{img}')
            encoding = face_recognition.api.face_encodings(image, model='large')
            # print(face_recognition.api.face_encodings(image, model='large'))
            if len(encoding) > 0:
                face_encodings.append(encoding[0])
            else:
                print('No face detected!')
                return
            
        all_face_encodings[folder] = face_encodings
        
    with open('./database/known_face_encodings', 'wb') as file:
        pickle.dump(all_face_encodings, file)

# generate_encodings("./photos")