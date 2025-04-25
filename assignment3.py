import glob
import os
import socket
import multiprocessing

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
    total_key_length = 0
    total_value_length = 0
    client_connections = 0

    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            client_connections += 1
            print(f"Accepted connection from {client_addr}")

            with client_conn:
                while True:
                    data = client_conn.recv(1024).decode('utf-8')
                    if not data:
                        break

                    operation = data[0]
                    key, value = None, None

                    # Parse the request
                    if operation == 'READ' or operation == 'GET':
                        key = data[2:]
                    elif operation == 'PUT':
                        key_value = data[2:].split(' ', 1)
                        if len(key_value) < 2:
                            response = "ERR invalid request"
                            client_conn.send(response.encode('utf-8'))
                            continue
                        key, value = key_value[0], key_value[1]

                    # Process the request
                    if operation == 'READ':
                        total_operations += 1
                        total_reads += 1

                        if key in tuple_space:
                            response = f"0{len(key) + len(tuple_space[key]) + 14} OK ({key}, {tuple_space[key]}) read"
                        else:
                            response = f"ERR {key} does not exist"
                    elif operation == 'GET':
                        total_operations += 1
                        total_gets += 1

                        if key in tuple_space:
                            response = f"0{len(key) + len(tuple_space[key]) + 16} OK ({key}, {tuple_space[key]}) removed"
                            del tuple_space[key]
                            total_key_length -= len(key)
                            total_value_length -= len(tuple_space[key])
                        else:
                            response = f"ERR {key} does not exist"
                    elif operation == 'PUT':
                        total_operations += 1
                        total_puts += 1

                        if key not in tuple_space:
                            tuple_space[key] = value
                            total_key_length += len(key)
                            total_value_length += len(value)
                            response = f"0{len(key) + len(value) + 14} OK ({key}, {value}) added"
                        else:
                            errors += 1
                            response = f"ERR {key} already exists"
                    else:
                        response = "ERR invalid operation"

                    # Send the response back to the client
                    client_conn.send(response.encode('utf-8'))

            total_clients += 1
            # Print server summary every 10 seconds or periodically
            print(f"Current tuple space size: {len(tuple_space)}")
            print(f"Total clients connected: {total_clients}")
            print(f"Total operations: {total_operations}, READs: {total_reads}, GETs: {total_gets}, PUTs: {total_puts}")

    except KeyboardInterrupt:
        # Handle graceful shutdown
        print("\nServer shutting down...")
        server_socket.close()


def main():
    """Main function to start the client and server."""

    # Start the server in a separate process
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()

    # Wait for the server to start
    time.sleep(1)

    # Find all client_*.txt files in the same directory
    client_files = glob.glob('client_*.txt')

    # Read and process each file
    for file in client_files:
        print(f"Processing {file}")
        # Send the request to the server (localhost, port 51234)
        send_request_to_server('localhost', 51234, file)

    # After all clients are done, wait a bit and then stop the server
    time.sleep(5)
    server_process.terminate()

if __name__ == '__main__':
    main()