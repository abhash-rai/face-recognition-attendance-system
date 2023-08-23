import numpy as np
import face_recognition

def image_encoder(image: np.ndarray) -> list:
    '''
    Encodes only the face portions of a single given image into 128-dimension face encoding
    Input -> (image) 1 Dimensional numpy array representation of an image
    Return -> Face encoding (List of NumPy array)
              If only 1 face in the picture then, returns a list of just 1 face encoding
              else, return list of multiple face encodings
    '''
    return face_recognition.api.face_encodings(image)

def image_encoder(image: np.ndarray) -> np.ndarray:
    '''
    Encodes only the face portion of a single given image into 128-dimension face encoding
    Input -> (image) 1 Dimensional numpy array representation of an image
    Return -> Face encoding (NumPy array)
    '''
    top, right, bottom, left = face_recognition.api.face_locations(image)
    face_only = image[top:bottom, left:right]
    return face_recognition.face_encodings(face_only)

def encode_multiple_images(images: list) -> list:
    '''
    Encodes a given list of np.ndarray image representation into a list of same length list of 128-dimension np.ndarray face encoding for each element in the given list
    Input -> (images) List of 1 Dimensional numpy array representation of images
    Return -> list of face encodings
    '''
    return [ image_encoder(image) for image in images]

def compare_with_database_encoding(database_encodings: list, unknown_face_encoding: np.ndarray):
    '''
    Compares 'unknown_face_encoding' with list of 'database_encodings'
    Return -> list of a euclidean distance for each comparison face
    '''
    pass

def main():
    '''
    Main script to run
    '''
    pass