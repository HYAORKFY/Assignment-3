import socket

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
    pass

def main():
    """Main function to start the client and server."""
    
    # Start the server in a separate process
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()

    # Wait for the server to start
    time.sleep("1")

    # Find all client_*.txt files in the same directory
    client_files = glob.glob('client_*.txt')

    # Read and process each file
    for file in client_files:
        print(f"Processing {file}")
        # Send the request to the server (localhost, port 51234)
        send_request_to_server('localhost', 51234, file)

    # After all clients are done, wait a bit and then stop the server
    time.sleep("5")
    server_process.terminate()

if __name__ == '__main__':
    main()