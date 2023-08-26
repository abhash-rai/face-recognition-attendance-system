import os
import numpy as np
from socket import *
import json




dictionary_encodings = {}

def get_encodings(encoding_path):
    for numpy_encoding in os.listdir(encoding_path):
        if numpy_encoding.endswith(".npy"):
            filename = numpy_encoding[:-4]  # Remove the '.npy' extension
            encoding_data = tuple(np.load(os.path.join(encoding_path, numpy_encoding)))  # Load the data from the numpy file
            encoding_data_tuple = str(encoding_data)  # Convert the NumPy array to a tuple
            dictionary_encodings[encoding_data_tuple] = filename  

    return dictionary_encodings


def send_json_encodings(chunksize,path):
    sock = socket()
    sock.bind(('', 5000))
    sock.listen(1)

    while True:
        print('Waiting for a client...')
        client, address = sock.accept()
        print(f'Client joined from {address}')
        with client:
            encodings_path = path
            encodings_data = get_encodings(encodings_path)
            encodings_json = json.dumps(encodings_data).encode()

            print('Sending data')

            total_bytes = len(encodings_json)
            num_chunks = (total_bytes + chunksize - 1) // chunksize

            client.sendall(str(num_chunks).encode() + b'\n')

            for i in range(0, total_bytes, chunksize):
                chunk = encodings_json[i:i + chunksize]
                client.sendall(chunk)

        print('Done.')


send_json_encodings(1_000_000,r"database\face_encodings")
