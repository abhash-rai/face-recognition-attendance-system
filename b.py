import socket
import time

def send_data_to_port(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    try:
        while True:
            client_socket.send(message.encode())
            print(f"Sent: {message}")
            time.sleep(1)  # Wait for 1 second before sending the next message
            
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Closing the connection.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    target_host = "localhost"  # Change this to the target IP address
    target_port = 9000       # Change this to the target port
    message_to_send = "Hello, server!"

    send_data_to_port(target_host, target_port, message_to_send)
