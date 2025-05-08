import socket
import threading

class TupleSpace:
    def __init__(self):
        self.tuple_space = {}
        self.lock = threading.Lock()

    def put(self, key, value):
        with self.lock:
            if key in self.tuple_space:
                return "024 ERR key already exists"
            if len(key) > 999 or len(value) > 999:
                return "024 ERR key or value too long"
            self.tuple_space[key] = value
            return f"0{len(key) + len(value) + 14} OK ({key}, {value}) added"

    def get(self, key):
        with self.lock:
            if key not in self.tuple_space:
                return "024 ERR key does not exist"
            value = self.tuple_space.pop(key)
            return f"0{len(key) + len(value) + 16} OK ({key}, {value}) removed"

    def read(self, key):
        with self.lock:
            if key not in self.tuple_space:
                return "024 ERR key does not exist"
            value = self.tuple_space[key]
            return f"0{len(key) + len(value) + 14} OK ({key}, {value}) read"

def start_server():
    host = 'localhost'
    port = 51234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server started on {host}:{port}")

    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            print(f"Accepted connection from {client_addr}")

            with client_conn:
                while True:
                    data = client_conn.recv(1024).decode('utf-8')
                    if not data:
                        break

                    parts = data.split(maxsplit=2)
                    if len(parts) < 2:
                        response = "024 ERR invalid request"
                        client_conn.send(response.encode('utf-8'))
                        continue

                    operation = parts[0]
                    key = parts[1]
                    value = parts[2] if len(parts) > 2 else None

                    if operation == 'GET':
                        response = tuple_space.get(key)
                    elif operation == 'PUT':
                        response = tuple_space.put(key, value)
                    elif operation == 'READ':
                        response = tuple_space.read(key)
                    else:
                        response = "024 ERR invalid operation"

                    client_conn.send(response.encode('utf-8'))

    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server_socket.close()

if __name__ == '__main__':
    tuple_space = TupleSpace()
    start_server()