import socket
import select
import sys
import queue
from resp import resp
from typing import List
from .commands.command import command_registry, Command

class RedisServer:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.server = None

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.bind((self.host, self.port))

    def start(self):
        self.connect()
        print(f"Starting server on {self.host}:{self.port}")
        self.server.listen(5)
        self.handle_clients()

    def form_response(self, req: List) -> str:
        name, args = req[0], []
        if len(req) > 1:
            args = req[1:]
        command_class: Command = command_registry[name.lower()]
        command = command_class(args)
        return command.execute()

    def handle_clients(self):
        _in = [self.server]
        out = []
        client_message_queues = {}

        while _in:
            incoming, outgoing, exceptions = select.select(_in, out, _in)
            for conn in incoming:
                if conn == self.server:
                    client_connection, client_address = self.server.accept()
                    print(f"Accepted connection from {client_address}")
                    client_connection.setblocking(False)
                    _in.append(client_connection)
                    client_message_queues[client_connection] = queue.Queue()
                else:
                    data = conn.recv(1024)
                    if data:
                        client_req = resp.deserializeMsg(data.decode())
                        print(f"Received array {client_req} from {conn.getpeername()}")
                        client_message_queues[conn].put(client_req)
                        if conn not in out:
                            out.append(conn)
                    else:
                        if conn in out:
                            out.remove(conn)
                        _in.remove(conn)
                        conn.close()
                        del client_message_queues[conn]

            for conn in outgoing:
                try:
                    next_msg = client_message_queues[conn].get_nowait()
                except queue.Empty:
                    out.remove(conn)
                else:
                    conn.send(self.form_response(next_msg).encode())
