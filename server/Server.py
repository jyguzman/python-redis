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
        print(f"starting server on {self.host}:{self.port}")
        self.server.listen(5)
        self.event_loop()

    def accept_client(self):
        client_connection, client_address = self.server.accept()
        print(f"Accepted connection from {client_address}")
        client_connection.setblocking(False)
        self.connections.append(client_connection)
        self.client_message_queues[client_connection] = queue.Queue()

    def remove_client(self, client):
        if client in self.client_messages:
            self.client_messages.remove(client)
        self.connections.remove(client)
        client.close()
        del self.client_message_queues[client]

    def event_loop(self):
        inputs = [self.server]
        outputs = []
        message_queues = {}
        while inputs:
            _in, out, exceptions = select.select(inputs, outputs, inputs)
            for conn in _in:
                if conn == self.server:
                    client_connection, client_address = conn.accept()
                    print(f"Accepted connection from {client_address}")
                    client_connection.setblocking(False)
                    inputs.append(client_connection)
                    message_queues[client_connection] = queue.Queue()
                else:
                    data = conn.recv(1024)
                    if data:
                        print(f"Received {data} from {conn.getpeername()}")
                        message_queues[conn].put(data)
                        if conn not in outputs:
                            outputs.append(conn)
                    else:
                        if conn in outputs:
                            outputs.remove(conn)
                        inputs.remove(conn)
                        conn.close()
                        del message_queues[conn]

            for conn in out:
                try:
                    next_msg = message_queues[conn].get_nowait()
                except queue.Empty:
                    # No messages waiting so stop checking for writability.
                    outputs.remove(conn)
                else:
                    print(sys.stderr, 'sending "%s" to %s' % (next_msg, conn.getpeername()))
                    conn.send(next_msg)

