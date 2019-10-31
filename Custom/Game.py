from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, gethostbyname, gethostname
from threading import Thread

from base64 import b64encode

HOST = (gethostbyname(gethostname()), 7503)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
SOCK.bind(HOST)
SOCK.listen(2)
print(HOST)


def serve(__conn):
    __request = __conn.recv(512)
    try:
        __request = __request.decode().split(' ')
        if __request[0] == "GET":
            if __request[1][1:] == '':
                with open("Game.html", 'rb') as __FILE:
                    __DATA = __FILE.read()
                    __FILE.close()
                    __conn.sendall(b"HTTP/1.1 200 OK\n\n" + __DATA)
            else:
                with open(__request[1][1:], 'rb') as __FILE:
                    __DATA = __FILE.read()
                    __FILE.close()
                    __conn.sendall(b"HTTP/1.1 200 OK\n\n" + __DATA)
        else:
            with open(__request[1][1:], 'rb') as __FILE:
                __DATA = __FILE.read()
                __FILE.close()
                __conn.sendall(b"HTTP/1.1 200 OK\n\n" + b64encode(__DATA))
    except (FileNotFoundError, IndexError):
        __conn.sendall(b"HTTP/1.1 404 Not Found")
    __conn.close()


while True:
    conn, addr = SOCK.accept()
    serve_thread = Thread(target=serve, args=[conn, ])
    serve_thread.start()
