import socket
import threading
import os
from datetime import datetime

if not os.path.exists("server_files"):
    os.mkdir("server_files")


def write_log(message):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"[{datetime.now()}] {message}\n")


def authenticate(username, password):
    with open("users.txt", "r") as file:
        for line in file:
            saved_user, saved_pass = line.strip().split(",")
            if username == saved_user and password == saved_pass:
                return True
    return False


def recv_line(conn):
    data = b""
    while not data.endswith(b"\n"):
        part = conn.recv(1)
        if not part:
            break
        data += part
    return data.decode().strip()


def handle_client(conn):
    credentials = recv_line(conn)
    username, password = credentials.split(",")

    if authenticate(username, password):
        conn.sendall(b"LOGIN_SUCCESS\n")
        write_log(f"{username} logged in successfully")
    else:
        conn.sendall(b"LOGIN_FAILED\n")
        write_log(f"{username} failed login attempt")
        conn.close()
        return

    command = recv_line(conn)

    if command == "UPLOAD":
        filename = recv_line(conn)
        path = os.path.join("server_files", filename)

        conn.sendall(b"READY\n")

        size_text = recv_line(conn)
        file_size = int(size_text)

        with open(path, "wb") as file:
            remaining = file_size
            while remaining > 0:
                chunk = conn.recv(min(1024, remaining))
                if not chunk:
                    break
                file.write(chunk)
                remaining -= len(chunk)

        conn.sendall(b"UPLOAD_OK\n")
        write_log(f"{username} uploaded {filename}")

    elif command == "DOWNLOAD":
        filename = recv_line(conn)
        path = os.path.join("server_files", filename)

        if os.path.exists(path):
            conn.sendall(b"FOUND\n")
            file_size = os.path.getsize(path)
            conn.sendall(f"{file_size}\n".encode())

            ready = recv_line(conn)
            if ready == "READY":
                with open(path, "rb") as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        conn.sendall(data)

                write_log(f"{username} downloaded {filename}")
        else:
            conn.sendall(b"NOT_FOUND\n")
            write_log(f"{username} requested missing file {filename}")

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8000))
server.listen(5)

print("SecureDocs server is running...")

while True:
    conn, address = server.accept()
    print("Connected to:", address)

    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()

