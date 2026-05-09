import socket

from pygame.image import fromstring
from converters import *
from Command import *
from Parameters import PORT
from GameData import GameData
from Entity import Entity

def connect(IP):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))

def client_main(client_socket):
    pass

def send_data(client_socket, data: list[Command]):
    data = str(data)
    client_socket.sendall(data.encode('utf-8'))

def recieve_data(client_socket) -> str:
    try:
        data = client_socket.recv(1024)
    except:
        data = None
    return data

def handle_data(data: str, entities: list[Entity]):
    data.split("$")
    data.replace("[","")
    data.replace("]", "")
    datalst = data.split(", ")
    for item in datalst:
        entity = string_to_entity(item)
        for ent in entities:
            if ent.id == entity.id:



def disconnect(client_socket):
    data = str([Command("disconnect", "disconnect").__str__()])
    client_socket.sendall(data.encode('utf-8'))
    client_socket.close()