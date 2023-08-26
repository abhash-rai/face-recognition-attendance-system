import json
import socket
import ast

def recieve_encodings(chunksize, ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_address, port)  # the server's IP address and port
    sock.connect(server_address)

    # Receive the number of chunks
    num_chunks_data = sock.recv(chunksize)
    num_chunks = int(num_chunks_data.decode())

    # Receive JSON data
    json_data = b""
    for _ in range(num_chunks):
        chunk = sock.recv(chunksize)
        if not chunk:
            break
        json_data += chunk

    # Decode and load the received JSON data
    encodings_data = json.loads(json_data.decode())

    print("JSON data received:", encodings_data)
    sock.close()
    data_base = {ast.literal_eval(key): val for key, val in encodings_data.items()}
    return data_base

database = recieve_encodings(1_000_000, '192.168.1.10', 5000)
print(database)
