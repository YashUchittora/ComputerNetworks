import socket
import threading
import sys

#configuration
HOST = '127.0.0.1'
PORT = 5555

running = True

def receive_messages(client_socket):
    global running
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                if running:
                    print("\n[SERVER] Disconnected from server.")
                break

            sys.stdout.write('\r\033[K' + message + '\n> ')
            sys.stdout.flush()

        except Exception:
            if running:
                print("\n[ERROR] Connection lost.")
            break

def start_client():
    global running
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        username = input("Enter your username: ").strip()
        while not username:
            print("Username cannot be empty.")
            username = input("Enter your username: ").strip()
        client.send(f"JOIN {username}".encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
        receive_thread.start()

        print("You can start chatting! Type /quit or QUIT to exit.\n")
        while True:
            msg = input("> ")

            if not msg.strip():
                continue  

            if msg.strip().upper() == "QUIT" or msg.strip() == "/quit":
                running = False
                client.send("QUIT".encode('utf-8'))
                break

            if msg.strip() == "/list":
                client.send("LIST".encode('utf-8'))
                continue

            client.send(f"MSG {msg}".encode('utf-8'))

    except ConnectionRefusedError:
        print("Could not connect to the server. Is it running?")

    except KeyboardInterrupt:
        print("\nExiting...")
        running = False
        try:
            client.send("QUIT".encode('utf-8'))
        except:
            pass  

    finally:
        running = False
        client.close()
        print("Disconnected.")

if __name__ == "__main__":
    start_client()
