import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Listen for at most 1 connection

    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from: {client_address}")
            
            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received: {data}")
            except KeyboardInterrupt:
                print("Keyboard interrupt detected. Closing the connection.")
            finally:
                client_socket.close()
                print("Connection closed.")
            
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing the server.")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    listening_host = "localhost"  # Listen on all available interfaces
    listening_port = 9000      # Port to listen on

    start_server(listening_host, listening_port)
