import pandas as pd
import numpy as np
import datetime
import socket
import json
import threading
import os 

class Server:

    def __init__(self):

        self.__students_csv_path = './database/students.csv'
        self.__students_csv = pd.read_csv(self.__students_csv_path)

        self.__attendance_csv_path = './database/attendance.csv'
        self.__attendance_csv = pd.read_csv(self.__attendance_csv_path).set_index('unique_identifier')
    
        self.__face_endocings_directory_path = './database/face_encodings/'
    
    def send_json_face_encodings(self, server_ip_address='localhost', server_port=5001, chunksize=100000):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip_address, server_port))
        server_socket.listen(1)
        
        print(f"\nSender listening on port {server_port}")
        print('Waiting for a session request...')
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"\nSession connected from: {addr[0]}:{addr[1]}")
            
            encodings_data = { str(tuple(np.load(self.__face_endocings_directory_path+encoded_face_id))):encoded_face_id.split('.')[0] for encoded_face_id in os.listdir(self.__face_endocings_directory_path) }
            encodings_json = json.dumps(encodings_data).encode()

            print('Sending data...')

            total_bytes = len(encodings_json)
            num_chunks = (total_bytes + chunksize - 1) // chunksize

            client_socket.sendall(str(num_chunks).encode() + b'\n')

            for i in range(0, total_bytes, chunksize):
                chunk = encodings_json[i:i + chunksize]
                client_socket.sendall(chunk)

            print('Face encodings data sent.\n')
            
            client_socket.close()

    def get_current_date_time(self) -> tuple:
        '''Gets the current date and time stamp, converts to string and returns both'''
        date_time = datetime.datetime.now()
        return (str(date_time.date()), str(date_time.time()))

    def init_attendance_today(self) -> None:
        date, _ = self.get_current_date_time()
        for student in self.__students_csv['unique_identifier']:
            self.__attendance_csv.loc[student] = [student.split('-')[0], date, np.nan, False]
        self.__attendance_csv.to_csv(self.__attendance_csv_path, index=True) # Saving the new data

    def make_attendance(self, student_id_time_dict: dict) -> None:
        '''Iterates over the given dict items and makes attendance'''
        for unique_identifier, time in student_id_time_dict.items():
            if self.__attendance_csv.loc[unique_identifier,'attendance'] == False:
                self.__attendance_csv.loc[unique_identifier,'time'] = time
                self.__attendance_csv.loc[unique_identifier,'attendance'] = True
        self.__attendance_csv.to_csv(self.__attendance_csv_path, index=True) # Saving the new data

    def recieve_identified_ids_timestamps(self, server_ip_address='localhost', server_port=5002, chunksize=1_000_000) -> dict:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip_address, server_port))
        server_socket.listen(1)  # Listen for at most 1 connection

        print(f"Server listening on {server_ip_address}:{server_port}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from: {client_address}")
                
                try:
                    while True:
                        data = client_socket.recv(1024).decode()
                        if not data:
                            break
                        received_dict = json.loads(data)
                        print("Received dictionary:", received_dict)
                        self.make_attendance(received_dict)
                except KeyboardInterrupt:
                    print("Keyboard interrupt detected. Closing the connection.")
                finally:
                    client_socket.close()
                    print("Connection closed.")
                
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Closing the server.")
        finally:
            server_socket.close()
            print("Server closed.\n")


def main():
    server = Server()

    while True:
        init_attendence_status = input(f'\nDo you want to initialize attendance for today? (y/n): ')
        init_attendence_status = init_attendence_status.lower()
        if init_attendence_status == 'y':
            server.init_attendance_today()
            print('Attendance initialized for all students with default absent. Attendance will be made present as students are identified!')
            break
        elif init_attendence_status == 'n':
            break
        else:
            print(f'Enter a valid command - y/n')

    send_json_face_encodings_thread = threading.Thread(target=server.send_json_face_encodings, args=('localhost', 5001, 1_000_000))
    recieve_student_identification = threading.Thread(target=server.recieve_identified_ids_timestamps, args=('localhost', 5002, 1_000_000))

    send_json_face_encodings_thread.start()
    recieve_student_identification.start()
    
    send_json_face_encodings_thread.join()
    recieve_student_identification.join()

main()