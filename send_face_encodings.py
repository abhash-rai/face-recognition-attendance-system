import os
import numpy as np
from socket import *
import json

face_endocings_directory_path = './database/face_encodings'

def send_json_face_encodings(server_ip_address, server_port, chunksize):
    sock = socket()
    sock.bind((server_ip_address, server_port))
    sock.listen(1)

    while True:
        print('Waiting for a client...')
        client, address = sock.accept()
        print(f'Client joined from {address}')
        with client:
            encodings_data = { str(tuple(np.load(face_endocings_directory_path+encoded_face_id))):encoded_face_id.split('.')[0] for encoded_face_id in os.listdir(face_endocings_directory_path) }
            encodings_json = json.dumps(encodings_data).encode()

            print('Sending data')

            total_bytes = len(encodings_json)
            num_chunks = (total_bytes + chunksize - 1) // chunksize

            client.sendall(str(num_chunks).encode() + b'\n')

            for i in range(0, total_bytes, chunksize):
                chunk = encodings_json[i:i + chunksize]
                client.sendall(chunk)

        print('Done.')

send_json_face_encodings(
    server_ip_address = '', 
    server_port = 5000, 
    chunksize = 1_000_000
)