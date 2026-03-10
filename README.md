# Simple Chat Application

## Overview
This project implements a simple multi-client chat application using TCP socket programming in Python. The system follows a client–server architecture where a server manages communication and multiple clients connect to it to exchange messages. Each client connects to the server, enters a username, and can send messages that are broadcast to other connected users. The server handles multiple clients simultaneously using threads.

## How to Run

### 1. Start the Server
Run the following command:
```
python server.py
```

The server will start listening on `127.0.0.1:5555`.

### 2. Start a Client
Open another terminal and run:
```
python client.py
```

Enter a username when prompted.

### 3. Start Chatting
Type messages and press Enter to send them to other connected users.

Useful commands:
```
/list  - show online users
/quit  - exit the chat
```
