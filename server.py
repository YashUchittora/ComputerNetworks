import socket
import threading
import logging
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5555

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

clients: dict[socket.socket, str] = {}

def broadcast(message, sender=None):
    for conn in clients:
        if conn != sender:
            try:
                conn.send(message.encode('utf-8'))
            except:
                pass

def remove_client(conn):
    if conn in clients:
        username = clients[conn]
        clients.pop(conn, None)
        msg = f"[SERVER] {username} left the chat"
        logging.info(msg)
        broadcast(msg)
    conn.close()

def handle_client(conn, addr):
    print("New connection:", addr)
    username = None

    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')

            if not msg:
                break

            if msg.startswith("JOIN "):
                username = msg[5:]
                clients[conn] = username

                join_msg = f"[SERVER] {username} joined the chat"
                logging.info(join_msg)

                conn.send("Welcome to the chat!".encode('utf-8'))
                broadcast(join_msg, conn)

            elif msg.startswith("MSG "):
                text = msg[4:]
                time_now = datetime.now().strftime('%H:%M')
                chat_msg = f"[{time_now}] {username}: {text}"

                logging.info(chat_msg)
                broadcast(chat_msg, conn)

            elif msg == "LIST":
                users = ", ".join(clients.values())
                conn.send(f"Online users: {users}".encode('utf-8'))

            elif msg == "QUIT":
                break

            else:
                conn.send("Unknown command".encode('utf-8'))

        except:
            break

    remove_client(conn)
    print("Connection closed:", addr)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server listening on", HOST, PORT)
    logging.info("Server started")

    while True:
        conn, addr = server.accept()
        logging.info(f"Connection from {addr}")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()
