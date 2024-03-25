import socket
import select
import sys
import queue

class RedisServer:
    def __init__(self, host = "localhost", port = 6379):
        self.host = host
        self.port = port
        self.server = None

        self.connections = []
        self.client_messages = []
        self.exceptions = []

        self.client_message_queues = {}

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)

        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def init_event_loop(self):


    def accept_client(self):
        client_connection, client_address = self.server.accept()
        print(f"Accepted connection from {client_address}")
        client_connection.setblocking(False)
        self.connections.append(client_connection)
        self.client_message_queues[client_connection] = queue.Queue()

    def remove_client(self, client):
        if client in self.client_messages:
            self.client_messages.remove(client)
        client.close()
        del self.client_message_queues[client]

    def event_loop(self):
        if self.server is None:
            self.connect()
        self.connections, self.client_messages, self.exceptions = select.select([self.server], [], [self.server])
        while self.connections:
            for conn in self.connections:
                if conn == self.server:
                    self.accept_client()
                else:
                    data = conn.recv(1024)
                    if data:
                        print(f"Received {data} from {conn.getpeername()}")
                        self.client_message_queues[conn].put(data)
                        if conn not in self.client_messages:
                            self.client_messages.append(conn)
                    else:
                        self.remove_client(conn)



        pass


