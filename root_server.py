import socket
import threading


def copy_to_nao(command):
    file = open("~", "w")
    file.write("whatever")
    file.close()


def handle_client(client_socket):
    data = client_socket.recv(1024)
    if not data:
        client_socket.close()
        return

    message = data.decode("utf-8")
    print(f"Received message: {message}")

    copy_to_nao(message)

    client_socket.sendall(
        (
            'Executed the command "'
            + message.split(";")[0]
            + '"'
            + " on "
            + message.split(";")[1]
        ).encode("utf-8")
    )

    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 5000
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    main()
