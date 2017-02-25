# -*- coding: utf-8 -*-
"""Client module to communicate with server module."""
import sys
import socket
from server import BUFFER_LENGTH

ADDRINFO = ('127.0.0.1', 5000, 2, 1, 6)


def client(msg):
    """Start a client looking for a connection at listening server."""
    infos = socket.getaddrinfo(*ADDRINFO)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    cli_sock = socket.socket(*stream_info[:3])
    cli_sock.connect(stream_info[-1])

    cli_sock.sendall(msg.encode('utf-8'))
    cli_sock.shutdown(socket.SHUT_WR)
    response_parts = []
    while True:
        part = cli_sock.recv(BUFFER_LENGTH)
        response_parts.append(part)
        if len(part) < BUFFER_LENGTH:
            break
    response = b''.join(response_parts).decode('utf-8')
    cli_sock.close()
    return response


if __name__ == '__main__':
    msg = sys.argv[1]
    print(client(msg))
