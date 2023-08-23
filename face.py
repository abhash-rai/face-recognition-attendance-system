import numpy as np

def image_path_to_numpy_array(image_paths: list) -> np.ndarray:
    '''
    Converts given 'image_paths' to a list of numpy array representation of those image paths
    Return -> list (of np.ndarray)
    '''
    pass

def image_encoder(image: np.ndarray) -> np.ndarray:
    '''
    Encodes a single given image into 128-dimension face encoding
    Input -> (image) 1 Dimensional numpy array representation of an image
    Return -> Face encoding (NumPy array)
    '''
    pass

def encode_multiple_images(images: list) -> list:
    '''
    Encodes a given list of np.ndarray image encoding into a list of same length list of 128-dimension np.ndarray face encoding for each element in the given list
    Input -> (images) List of 1 Dimensional numpy array representation of images
    Return -> list of face encodings
    '''

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