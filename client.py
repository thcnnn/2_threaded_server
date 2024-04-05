import socket
import threading
import os
import json
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
users = load_users()
def listen(s: socket.socket):
    while True:
        msg = s.recv(2048)
        print('\r\r' + msg.decode() + '\n' + f'you: ', end='')


def connect(host='127.0.0.1', port=9090):
    s = socket.socket()

    s.connect((host, port))

    threading.Thread(target=listen, args=(s,), daemon=True).start()

    while True:
        msg = input(f'you: ')
        s.send(msg.encode())


if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')
    connect()

