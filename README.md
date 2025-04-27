# Assignment-3
 My system and network homework for assignment3


## Overview
This project implements a client/server networked system that supports a "tuple space". The server handles multiple clients concurrently, processing requests to include, read, or delete tuples. Each tuple is a key-value pair with unique keys.

## Features
- **Thread-safe TupleSpace**: Ensures thread-safe operations using `threading.Lock`.
- **Concurrent Client Handling**: Supports multiple clients connecting and sending requests simultaneously.
- **Request Types**: Supports `PUT`, `GET`, and `READ` operations.
- **Error Handling**: Properly handles errors such as key existence, invalid requests, and long keys/values.

## Running the Server
Make sure that assignment3.py,assignment3test.py and the txt file for data are in the same file
When you are running assignment3,py, run assignment3test.py at the same time.
