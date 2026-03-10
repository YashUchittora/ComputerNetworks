import socket
import threading

HOST = '127.0.0.1'
PORT = 5555


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except:
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("Connected to server.")

        username = input("Enter username: ")
        client.send(f"JOIN {username}".encode('utf-8'))

        thread = threading.Thread(target=receive_messages, args=(client,))
        thread.start()

        while True:
            msg = input()

            if msg.lower() == "/quit":
                client.send("QUIT".encode('utf-8'))
                break

            if msg.lower() == "/list":
                client.send("LIST".encode('utf-8'))
            else:
                client.send(f"MSG {msg}".encode('utf-8'))

    except:
        print("Unable to connect to server.")

    finally:
        client.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_client()
