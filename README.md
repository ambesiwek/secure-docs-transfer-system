# Secure-docs-transfer-system
Python client-server file transfer system with authentication, multithreading, and logging.
# Secure Docs Transfer System

A Python-based client-server file transfer system that allows authenticated users to upload and download files through a central server.

Features
- User authentication using a `users.txt` file
- TCP client-server communication
- File upload to the server
- File download from the server
- Multithreaded server to handle multiple clients
- Activity logging using `logs.txt`

Technologies Used
- Python
- Socket programming
- Threading
- File handling
- OS module
- Datetime module

Project Structure
secure-docs-transfer-system/
- client.py
- server.py
- users.txt
- logs.txt
- server_files/
- README.md

How It Works
1. The server starts and listens for incoming client connections.
2. The client connects to the server.
3. The user enters a username and password.
4. The server checks the credentials from `users.txt`.
5. If login is successful, the client can choose to:
   - upload a file to the server
   - download a file from the server
6. The server records activity in `logs.txt`.

The example Login
Username:
`admin`

Password:
`1234`

Learning Goals
this project demonstrates:
- how TCP socket communication works
- how a multithreaded server handles multiple clients
- how file transfer works in Python
- how authentication can be added to a client-server application
- how logging can be used to track server activity

Future Improvements:
- Add SSL/TLS encryption
- Create a graphical user interface
- Store users in a database
- Add file type restrictions
- Add better error handling

Author:
Created by Ambesiwe
