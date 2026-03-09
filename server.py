import socket
import threading
import logging
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5555

#for logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('server.log'),   
        logging.StreamHandler()              
    ]
)
clients = {}

def broadcast(message, sender_conn=None):
    for conn in list(clients.keys()):
        if conn != sender_conn:
            try:
                conn.send(message.encode('utf-8'))
            except:
                pass

def remove_client(conn):
    if conn in clients:
        username = clients[conn]
        clients.pop(conn)  
        leave_msg = f"[SERVER] {username} has left the chat."
        logging.info(f"{username} has left the chat.")
        broadcast(leave_msg)  
        try:
            conn.close()
        except:
            pass  

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    username = None  

    try:
        while True:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break  

            msg = msg.strip()
            if not msg:
                continue  

            if msg.startswith("JOIN "):
                username = msg[5:].strip()
                clients[conn] = username

                join_msg = f"[SERVER] {username} has joined the chat!"
                logging.info(f"{username} joined from {addr}")

                conn.send("Welcome to the server! Type 'QUIT' to exit. Send '/list' to see online users.".encode('utf-8'))

                broadcast(join_msg, conn)

            elif msg.startswith("MSG "):
                if username is None:
                    conn.send("[SERVER] Error: You must JOIN before sending a MSG.".encode('utf-8'))
                else:
                    text = msg[4:]
                    time_now = datetime.now().strftime('%H:%M')
                    chat_msg = f"[{time_now}] [{username}]: {text}"
                    logging.info(f"MSG from {username}: {text}")
                    broadcast(chat_msg, conn)

            elif msg == "LIST":
                if not clients:
                    user_list = "[SERVER] No users online."
                else:
                    names = ', '.join(clients.values())
                    user_list = f"[SERVER] Online users ({len(clients)}): {names}"
                conn.send(user_list.encode('utf-8'))
                logging.info(f"{username} requested user list")

            elif msg == "QUIT":
                break

            else:
                conn.send("[SERVER] Unknown command. Use JOIN, MSG, LIST, or QUIT.".encode('utf-8'))

    except ConnectionResetError:
        pass  
    except Exception as e:
        logging.error(f"Exception for {addr}: {e}")
    finally:
        remove_client(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  

    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            logging.info(f"New connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    logging.info("Server is starting...")
    start_server()
