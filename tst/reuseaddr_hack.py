import socket


socket.socket._bind = socket.socket.bind


def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)


socket.socket.bind = my_socket_bind
