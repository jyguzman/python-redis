import socket
import sys

class RedisClient:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_address)

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    server_address = ('localhost', 6379)

    # Connect the socket to the port where the server is listening
    print(sys.stderr, 'connecting to %s port %s' % server_address)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    message = input("Send a message: ")

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
