import socket


def recv_data(sock: socket.socket):
    data = b''
    while b'\r\n' not in data:
        data += sock.recv(1024)
    return data.split(b'\r\n')[0].decode()


def send_data(sock: socket.socket, data):
    sock.send(data.encode()+b'\r\n')

