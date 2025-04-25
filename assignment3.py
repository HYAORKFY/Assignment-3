import glob
import os
import socket
import threading
import time

def send_request_to_server(host, port, filename):
    """Send each line of the file as a request to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    with open(filename, 'r') as f:
        for line in f:
            # Strip the line of any leading/trailing whitespace
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Send the request to the server
            client_socket.send(line.encode('utf-8'))

            # Wait for the response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Sent: {line}, Received: {response}")

    # Close the connection
    client_socket.close()

def start_server():
    """The TCP server that will handle client connections."""
    host = 'localhost'
    port = 51234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Keep track of some statistics
    total_clients = 0
    total_operations = 0
    total_reads = 0
    total_gets = 0
    total_puts = 0
    errors = 0

    # The tuple space
    tuple_space = {}

    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            total_clients += 1
            print(f"Accepted connection from {client_addr}")

            with client_conn:
                while True:
                    data = client_conn.recv(1024).decode('utf-8')
                    if not data:
                        break

                    # Parse the request
                    parts = data.split(maxsplit=2)
                    if len(parts) < 2:
                        response = "024 ERR invalid request"
                        client_conn.send(response.encode('utf-8'))
                        continue

                    operation = parts[0]
                    key = parts[1]
                    value = parts[2] if len(parts) > 2 else None

                    # Process the request
                    if operation == 'GET':
                        total_operations += 1
                        total_gets += 1

                        if key in tuple_space:
                            response = f"0{len(key) + len(tuple_space[key]) + 16} OK ({key}, {tuple_space[key]}) removed"
                            del tuple_space[key]
                        else:
                            response = f"024 ERR {key} does not exist"
                    elif operation == 'PUT':
                        total_operations += 1
                        total_puts += 1

                        if key not in tuple_space:
                            tuple_space[key] = value
                            response = f"0{len(key) + len(value) + 14} OK ({key}, {value}) added"
                        else:
                            errors += 1
                            response = f"024 ERR {key} already exists"
                    elif operation == 'READ':
                        total_operations += 1
                        total_reads += 1

                        if key in tuple_space:
                            response = f"0{len(key) + len(tuple_space[key]) + 14} OK ({key}, {tuple_space[key]}) read"
                        else:
                            response = f"024 ERR {key} does not exist"
                    else:
                        response = "024 ERR invalid operation"

                    # Send the response back to the client
                    client_conn.send(response.encode('utf-8'))

            # Print server summary every 10 seconds or periodically
            print(f"Current tuple space size: {len(tuple_space)}")
            print(f"Total clients connected: {total_clients}")
            print(f"Total operations: {total_operations}, READs: {total_reads}, GETs: {total_gets}, PUTs: {total_puts}")

    except KeyboardInterrupt:
        # Handle graceful shutdown
        print("\nServer shutting down...")
        server_socket.close()

def main():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait for the server to start

    time.sleep(1)

    # Find all client_*.txt files in the same directory
    client_files = glob.glob('client_*.txt')

    # Read and process each file
    for file in client_files:
        print(f"Processing {file}")
        # Send the request to the server (localhost, port 51234)
        send_request_to_server('localhost', 51234, file)

    time.sleep(5)

if __name__ == '__main__':
    main()