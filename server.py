import socket
import json
from threading import Thread

port = 9090
sock = socket.socket()
sock.bind(('', port))
print("Server is starting")
sock.listen(5)
print("Port", port, "is listening")
history = []
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(user_ip, user_name):
    with open("users.json", "r") as file:
        data = json.load(file)
        data[user_ip] = user_name
        with open("users.json", "w") as outfile:
            json.dump(data, outfile, indent=2)

def broadcast(message, sender_conn):
    for client_conn in clients.keys():
        if client_conn != sender_conn:
            client_conn.send(message.encode())

clients = {}
def handle_client(conn, addr):
    global history
    users = load_users()
    client_ip = addr[1]

    if client_ip in users:
        conn.send(f"Добрый день, {users[client_ip]}!\n".encode())
    else:
        conn.send("Представьтесь: ".encode())
        name = conn.recv(1024).decode().strip()
        conn.send("Регистрация успешна.".encode())
        save_users(client_ip, name)

    clients[conn] = name

    while True:
        try:
            message = conn.recv(1024).decode()
            print(message)
            if not message:
                break
            broadcast(f"{name}: {message}", conn)
            history.append(message)
        except ConnectionResetError:
            break

    del clients[conn]
    conn.close()

while True:
    conn, addr = sock.accept()
    print("Client is accepted")
    print("Client address:", addr[0])
    print("Client port:", addr[1])
    print(history)
    Thread(target=handle_client, args=(conn, addr)).start()
