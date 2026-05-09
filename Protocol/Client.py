import socket
from Parameters import PORT

def connect(IP):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))


def send_data(client_socket, data):
    pass

def recieve_data(client_socket):
    client_socket.recv(1024)
    pass

def disconnect():
    pass