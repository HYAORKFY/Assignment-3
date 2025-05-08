# Assignment - 3
My system and network homework for assignment3

## Overview
This project implements a client/server networked system that supports a "tuple space". The server can handle requests from multiple clients concurrently, including operations such as inserting, reading, or deleting tuples. Each tuple is a key - value pair, and the keys are unique.

## Features
- **Thread - safe TupleSpace**: Utilizes `threading.Lock` to ensure thread - safe operations in the tuple space, guaranteeing data consistency and correctness in a multi - threaded environment.
- **Concurrent Client Handling**: Supports multiple clients connecting to the server and sending requests simultaneously. The server creates an independent thread for each client to handle requests, avoiding request interleaving and improving the system's concurrent processing ability.
- **Request Types**: Supports three operations: `PUT`, `GET`, and `READ`. `PUT` is used to add a new tuple to the tuple space; `GET` is used to retrieve and delete a tuple with a specified key; `READ` is used to read a tuple with a specified key without deletion.
- **Error Handling**: Can properly handle various error situations, such as key already existing (when performing a `PUT` operation), key not existing (when performing a `READ` or `GET` operation), invalid request format, and long keys/values, and return corresponding error messages.

## Running the Server
1. Ensure that `server.py`, `client.py`, and the text file containing requests are in the same directory.
2. First, start the server. Run `python server.py` in the command line. After the server starts, it will listen on the specified port (e.g., 51234) and wait for client connections.
3. Then, start the clients. For each client, run `python client.py` in the command line. The client will read the requests from the specified text file and send them to the server, and display the sending and receiving results of each request.

## Running Tests
1. Run the concurrent access test script `clienttest.py`, which can simulate multiple clients accessing the server simultaneously to test the server's performance and correctness under concurrent conditions. Run `python clienttest.py` in the command line to start the test.
2. When testing, ensure that the server has been started and is running normally. The test script will automatically connect to the server and send preset requests.

## Precautions
1. The port number that the server listens on must be between 50000 and 59999. Using other ports may cause connection failures.
2. Each line in the client request file represents a request, and the request format must meet the requirements. Otherwise, the client will output an error message and ignore the request.
3. Both the key and value of a tuple are strings, with a maximum length of 999 characters each. The total length of the key - value pair (as a single string separated by a space) cannot exceed 970 characters. 