import face_recognition
import cv2
import os

def face_encodings_generator(
    face_images: list, 
    role: str,
    id: int,
    student_images_path='./user_images/students',
    staff_images_path='./user_images/staffs'
):
    image_count = 0
    
    # By deafult the given images are saved into 'user_images' folder in the root directory to access later.
    os.makedirs(student_images_path, exist_ok=True)
    os.makedirs(staff_images_path, exist_ok=True)

    face_encodings = []

    for face in face_images:
        image = cv2.imread(face)

        encoding = face_recognition.api.face_encodings(image, model='large') # Detect faces and generating encodings in the image

        if len(encoding) == 0:
            print(f"0 faces detected in '{face}' image. Replace the image with one which has face of a single person clearly visible!")
            exit()

        elif len(encoding) == 1:
            face_encodings.append(encoding[0])

            # Also saving only the face portion of the image so as to be able to access it later if need be
            face_locations = face_recognition.face_locations(image)
            top, right, bottom, left = face_locations[0]
            cropped_face = image[top:bottom, left:right] # Crop the face from the image
            if role == 'student':
                cv2.imwrite(f'{student_images_path}/{id}-{image_count}.jpg', cropped_face) # Save
            elif role == 'staff':
                cv2.imwrite(f'{staff_images_path}/{id}-{image_count}.jpg', cropped_face) # Save

        elif len(encoding) > 1:
            print(f"More than 1 faces detected in '{face}' image. Replace the image with one which has face of a single person clearly visible!")
            exit()

        image_count += 1
            
    return face_encodings

def student_entry(
    student_id: int,
    university_code: int,
    first_name: str,
    middle_name: str,
    last_name: str,
    front_face_image: str,
    left_face_image: str,
    right_face_image: str,
):
    # Check if student id already exists here

    # Generating face encodings of all three angles of faces
    face_encodings = face_encodings_generator(
        face_images = [left_face_image, front_face_image, right_face_image],
        role = "student",
        id = student_id,
    )

    # Make record to database here

    return face_encodings

def staff_entry(
    staff_id: int,
    first_name: str,
    middle_name: str,
    last_name: str,
    front_face_image: str,
    left_face_image: str,
    right_face_image: str,
):
    # Check if student id already exists here

    # Generating face encodings of all three angles of faces
    face_encodings = face_encodings_generator(
        face_images = [left_face_image, front_face_image, right_face_image],
        role = "staff",
        id = staff_id,
    )

    # Make record to database here

    return face_encodings