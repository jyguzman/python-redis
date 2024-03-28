import socket
from resp.resp import serializeRequest, deserialize

class RedisClient:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        print(f"Connected to Redis on {self.host}:{self.port}")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def end(self):
        self.client_socket.close()

    def run(self):
        client_in = input(f"{self.host}:{self.port}> ")
        while client_in.lower().strip() != 'bye':
            self.client_socket.send(serializeRequest(client_in).encode())  # send message
            server_response = self.client_socket.recv(1024).decode()  # receive response

            print('Received from redis: ' + server_response)  # show in terminal

            client_in = input(f"{self.host}:{self.port}> ")  # again take input
        self.end()

    def start(self):
        self.connect()
        self.run()


if __name__ == "__main__":
    client = RedisClient()
    client.connect()
    client.run()
