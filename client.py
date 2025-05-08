import glob
import os
import socket
import threading
import time
import subprocess

def send_request_to_server(host, port, filename):
    """Send each line of the file as a request to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            client_socket.send(line.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Sent: {line}, Received: {response}")

    client_socket.close()

def main():
    # Start the server in a separate process
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(1)

    client_files = glob.glob('client_*.txt')
    for file in client_files:
        print(f"Processing {file}")
        send_request_to_server('localhost', 51234, file)

    time.sleep(5)

def start_server():
    """Start the server in a separate process."""
    subprocess.Popen(['python', 'server.py'])

if __name__ == '__main__':
    main()