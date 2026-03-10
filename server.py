import socket
import threading
import logging
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5555

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M',
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

clients = {}

def broadcast(message, sender=None):
    for conn in list(clients.keys()):
        if conn != sender:
            try:
                conn.send(message.encode('utf-8'))
            except:
                pass

def remove_client(conn):
    if conn in clients:
        username = clients.pop(conn)
        msg = f"[SERVER] {username} left the chat."
        logging.info(msg)
        broadcast(msg)
    conn.close()

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    username = None

    try:
        while True:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break

            msg = msg.strip()

            if msg.startswith("JOIN "):
                username = msg[5:]
                clients[conn] = username

                join_msg = f"[SERVER] {username} joined the chat"
                logging.info(join_msg)

                conn.send("Welcome to the chat!".encode('utf-8'))
                broadcast(join_msg, conn)

            elif msg.startswith("MSG "):
                if username:
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
        pass
    finally:
        remove_client(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        logging.info(f"Connection from {addr}")

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    logging.info("Server starting...")
    start_server()
