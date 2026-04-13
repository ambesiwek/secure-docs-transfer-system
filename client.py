import socket
import os

def recv_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        part = sock.recv(1)
        if not part:
            break
        data += part
    return data.decode().strip()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8000))

username = input("Enter your username: ")
password = input("Enter your password: ")

credentials = username + "," + password + "\n"
client.sendall(credentials.encode())

login_response = recv_line(client)
print("Server:", login_response)

if login_response == "LOGIN_FAILED":
    client.close()
else:
    choice = input("Enter command (UPLOAD/DOWNLOAD): ").upper()
    client.sendall((choice + "\n").encode())

    if choice == "UPLOAD":
        filename = input("Enter file name to upload: ")
        client.sendall((filename + "\n").encode())

        ready = recv_line(client)

        if ready == "READY":
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                client.sendall(f"{file_size}\n".encode())

                with open(filename, "rb") as file:
                    while True:
                        data = file.read(1024)
                        if not data:
                            break
                        client.sendall(data)

                response = recv_line(client)
                print("Server:", response)
            else:
                print("File does not exist.")

    elif choice == "DOWNLOAD":
        filename = input("Enter file name to download: ")
        client.sendall((filename + "\n").encode())

        status = recv_line(client)

        if status == "FOUND":
            file_size = int(recv_line(client))
            client.sendall(b"READY\n")

            with open("downloaded_" + filename, "wb") as file:
                remaining = file_size
                while remaining > 0:
                    data = client.recv(min(1024, remaining))
                    if not data:
                        break
                    file.write(data)
                    remaining -= len(data)

            print("File downloaded successfully.")
        else:
            print("File not found on server.")

    else:
        print("Invalid command.")

client.close()