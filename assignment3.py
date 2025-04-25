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
                    if operation == 'R' or operation == 'G':
                        key = data[2:]
                    elif operation == 'P':
                        key_value = data[2:].split(' ', 1)
                        if len(key_value) < 2:
                            response = "ERR invalid request"
                            client_conn.send(response.encode('utf-8'))
                            continue
                        key, value = key_value[0], key_value[1]

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