import socket


class MyClass(GeneratedClass):
    def handle_client(client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode("utf-8")
            print("Received message:")

            response = ""
            if message == "handshake":
                response = 'Welcome to the server. To see the list of avaliable commands type "help".'
            elif message == "close":
                break

            elif message == "help":
                response = (
                    "The avaliable commands are:\n handshake, \n move, \n talk\n close"
                )

            elif message.split(" ")[0] == "talk":
                if len(message.split()) != 2:
                    response = 'Wrong amount of arguments! Usage: "talk Text"'
                else:
                    self.tts.say(message.split(" ")[1])
                    response = "Sent the command to the nao."

            # elif message.split(" ")[0] == "move":
            # response = handleInputWithNum(message, "move 90-y", ["x", "y"])

            else:
                response = (
                    message
                    + ' wasn\'t recognised. Type "help" to see the avaliable commands.'
                )
            response += "\n"
            client_socket.sendall(response.encode("utf-8"))
        client_socket.close()

    def __init__(self):
        GeneratedClass.__init__(self)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = "10.0.0.149"
        port = 80
        server_socket.bind((host, port))
        server_socket.listen(5)

        self.tts = ALProxy("ALTextToSpeech")

        self.tts.say("Server started")

        while True:
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from")
            handle_client(client_socket)

    def onLoad(self):
        # put initialization code here
        pass

    def onUnload(self):
        # put clean-up code here
        pass

    def onInput_onStart(self):
        # self.onStopped() #activate the output of the box
        self.tts.say("Hello world!")
        pass

    def onInput_onStop(self):
        self.onUnload()  # it is recommended to reuse the clean-up as the box is stopped
        self.onStopped()  # activate the output of the box
