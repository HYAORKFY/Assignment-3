import threading
import socket

def client_thread(host, port, requests):
    # Function for each client thread to send requests and receive responses
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        for request in requests:
            client_socket.send(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Sent: {request}, Received: {response}")

        client_socket.close()
    except Exception as e:
        print(f"Client thread encountered an error: {e}")