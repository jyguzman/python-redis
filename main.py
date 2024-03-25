from server.Server import RedisServer
server = RedisServer()
server.connect()
# import select
# import socket
# import sys
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # Prevent from "address already in use" upon server restart
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
# # Bind the socket to the port
# server_address = ('localhost', 10000)  # Use your port here
# print('starting up on {} port {}'.format(*server_address))
# server_socket.bind(server_address)
#
# # Listen for incoming connections
# server_socket.listen()
#
# # Sockets from which we expect to read
# inputs = [server_socket]
#
# # Sockets to which we expect to write
# outputs = []
#
# while inputs:
#     # Wait for at least one of the sockets to be ready for processing
#     readable, writable, exceptional = select.select(inputs, outputs, inputs)
#
#     # Handle inputs
#     for s in readable:
#         if s is server_socket:
#             # A "readable" server socket is ready to accept a connection
#             connection, client_address = s.accept()
#             print('new connection from', client_address)
#             connection.setblocking(0)
#             inputs.append(connection)
#         else:
#             data = s.recv(1024)
#             if data:
#                 # A readable client socket has data
#                 print('received {!r} from {}'.format(data, s.getpeername()))
#                 # Add output channel for response
#                 if s not in outputs:
#                     outputs.append(s)
#             else:
#                 # Interpret empty result as closed connection
#                 print('closing', client_address)
#                 if s in outputs:
#                     outputs.remove(s)
#                 inputs.remove(s)
#                 s.close()
#
#     # Handle outputs
#     for s in writable:
#         # Send response data here
#         # Ensure to remove from outputs after sending
#         pass
#
#     # Handle "exceptional conditions"
#     for s in exceptional:
#         print('handling exceptional condition for', s.getpeername())
#         # Stop listening for input on the connection
#         inputs.remove(s)
#         if s in outputs:
#             outputs.remove(s)
#         s.close()