import socket

# import threading

# ROOT_SERVER = "127.0.0.1"
# ROOT_PORT = 5000
# NAO = "10.0.0.23"


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# def sendToNao(command):
#    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# c.connect((ROOT_SERVER, ROOT_PORT))
# c.sendall((command + ";" + NAO).encode("utf-8"))
# return c.recv(1024).decode("utf-8")


def handleInputWithNum(message, usage, directions):
    if len(message.split(" ")) != 2:
        return "Wrong amount of arguments! Usage: " + '"' + usage + '"'
    else:
        arg = message.split(" ")[1]

        if len(arg.split("-")) != 2:
            return "Wrong amount of arguments! Usage: " + '"' + usage + '"'

        amount = arg.split("-")[0]
        direction = message.split("-")[1]

        if direction not in directions:
            return (
                "Unknown direction: "
                + direction
                + ". Try "
                + ",".join(directions)
                + "."
            )

        if not isNumber(amount):
            return "The amount wasn't a number."

        return "Sent the command to the nao.\n"


def handle_client(client_socket):

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode("utf-8")
        print(f"Received message: {message}")

        response = ""
        if message == "handshake":
            response = 'Welcome to the server. To see the list of avaliable commands type "help".'
        elif message == "help":
            response = "The avaliable commands are:\n handshake, \n move, \n talk"

        elif message.split(" ")[0] == "talk":
            if len(message.split()) != 2:
                response = 'Wrong amount of arguments! Usage: "talk Text"'
            else:
                # sendToNao(message)
                response = "Sent the command to the nao."

        elif message.split(" ")[0] == "move":
            response = handleInputWithNum(message, "move 90-y", ["x", "y"])

        else:
            response = (
                message
                + ' wasn\'t recognised. Type "help" to see the avaliable commands.'
            )
        response += "\n"
        client_socket.sendall(response.encode("utf-8"))
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        handle_client(client_socket)


if __name__ == "__main__":
    main()
