import socket


def recv_data(sock: socket.socket):
    data = b''
    while b'\r\n' not in data:
        new_data = sock.recv(1024)
        data += new_data
        if new_data == b'':
            return data
    return data.split(b'\r\n')[0].decode()


def send_data(sock: socket.socket, data):
    sock.send(data.encode()+b'\r\n')

