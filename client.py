import socket
import threading


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "10.0.0.149"
    port = 80
    client_socket.connect((host, port))

    first = True
    while True:
        message = ""
        if first:
            print("Sent handshake")
            message = "handshake"
            first = False
        else:
            message = input("Message: ").lower()

        client_socket.sendall(message.encode("utf-8"))
        data = client_socket.recv(1024)
        response = data.decode("utf-8")
        print(f"Server response: {response}")


if __name__ == "__main__":
    main()
