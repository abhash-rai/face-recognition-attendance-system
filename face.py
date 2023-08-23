import numpy as np
import face_recognition
import os
import cv2

def image_path_to_numpy_array(image_paths: list) -> np.ndarray:
    '''
    Converts given 'image_paths' to a list of numpy array representation of those image paths
    Return -> list (of np.ndarray)
    '''

    # Initialized an empty list to store list of known face encodings
    known_image_encodings=[]

    # Converting and then adding encodings of each image in the intialized list
    for image in image_paths:
        image=face_recognition.load_image_file(image)
        known_image_encodings.append(image)
        
    return known_image_encodings

def image_encoder(image: np.ndarray) -> np.ndarray:
    '''
    Encodes a single given image into 128-dimension face encoding
    Input -> (image) 1 Dimensional numpy array representation of an image
    Return -> Face encoding (NumPy array)
    '''
    pass

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

def main(paths):
    '''
    Main script to run
    '''
    list_of_paths = [str(f"{paths}\{path}") for path in os.listdir(paths)]
    return image_path_to_numpy_array(list_of_paths)

def capture_a_frame():
    videoCaptureObject = cv2.VideoCapture(0)
    result=True
    while(result):
        ret,frame=videoCaptureObject.read()
        frame1=cv2.imwrite("newframe.jpg",frame)
        result=False
    videoCaptureObject.release()
    cv2.destroyAllWindows()
    return frame1
    
