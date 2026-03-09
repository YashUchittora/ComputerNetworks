# Simple Chat Application

Computer Networks – Programming Assignment  
Student: Yash Chittora

## Project Overview

This project implements a simple multi-client chat application using TCP socket programming. The application follows a client–server architecture where a central server manages communication and multiple clients connect to it to exchange messages.

The server listens for incoming connections and allows multiple clients to join the chat simultaneously. Each client connects to the server, selects a username, and can send messages that are broadcast to all other connected users.

The project demonstrates important networking concepts such as TCP communication, client–server architecture, concurrency using threads, and basic protocol design.

---

## Features

- Multiple clients can connect to the server simultaneously
- Real-time messaging between connected users
- Join and leave notifications
- List of online users
- Message timestamps
- Server logging for connections and messages
- Graceful handling of client disconnections

---

## Technologies Used

- Python
- TCP Sockets
- Python Socket Library
- Threading Module
- Logging Module

---

## Project Structure

```
chat-app/
│
├── server/
│   └── server.py
│
├── client/
│   └── client.py
│
├── README.md
└── Report.pdf
```

---

## How to Run the Application

### 1. Start the Server

Run the following command in the server directory:

```
python server.py
```

You should see:

```
[LISTENING] Server is listening on 127.0.0.1:5555
```

---

### 2. Start a Client

Open another terminal and run:

```
python client.py
```

Enter a username when prompted.

Example:

```
Enter your username: Alice
```

---

### 3. Start Chatting

Users can send messages that will be broadcast to other connected clients.

Example:

```
> Hello everyone
```

---

## Available Commands

| Command | Description |
|--------|-------------|
| JOIN `<username>` | Registers the user with the server |
| MSG `<message>` | Sends a chat message |
| LIST | Displays currently connected users |
| QUIT | Leaves the chat |

Client shortcuts:

```
/list   -> show online users
/quit   -> exit the chat
```

---

## Communication Protocol

The system uses a simple text-based protocol between the client and the server.

Example messages:

```
JOIN Alice
MSG Hello everyone
LIST
QUIT
```

The server reads the command and performs the appropriate action such as broadcasting messages or returning the list of users.

---

## Concurrency Model

The server uses a **multi-threaded model** to handle multiple clients simultaneously. When a new client connects, a new thread is created to manage communication with that client.

Each client thread listens for messages independently, allowing multiple users to chat at the same time without blocking the server.

---

## Testing

The application was tested under the following scenarios:

- Multiple clients joining the chat
- Simultaneous messaging from different users
- Client leaving the chat
- Unexpected client disconnection
- Server stability with multiple connections

The server successfully handled these cases and continued running without crashing.

---

## Optional Features Implemented

- Message timestamps
- Online user list command
- Server logging for events and messages

---

## Conclusion

This project helped in understanding the fundamentals of network programming and client–server communication. It provided hands-on experience with TCP sockets, threading, and real-time message exchange between multiple clients.

The implementation demonstrates how distributed systems allow multiple users to communicate efficiently over a network.
