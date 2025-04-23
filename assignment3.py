import socket

def send_request_to_server(host, port, filename):
    """Send each line of the file as a request to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.close()


def start_server():
    """The TCP server that will handle client connections."""
    pass

def main():
    """Main function to start the client and server."""
    pass

if __name__ == '__main__':
    main()