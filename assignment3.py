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
    pass

if __name__ == '__main__':
    main()