# TCPChatRoom


TCP Chat Room Terminal is a simple Python-based client-server chat application using the TCP/IP protocol. It allows multiple clients to connect to a server and engage in real-time text-based communication.

## Table of Contents

- [Features]
- [Prerequisites]
- [Usage]
- [Commands]


## Features

- Real-time text-based communication
- Private messaging between clients
- Display of connected clients
- Graceful handling of client disconnection

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (version 3.9)



## How to use
Depending on you set up you can run the python files by simply clicking on them or you will have to naviagate within terminal to the directory that holds the server and client file and do the following:

Start the server:
python server.py

Run multiple instances of the client:
python client.py

For each instance of client:
Enter a unique name for each client when prompted.

Start chatting!

## Commands
Public Message:
Simply type your message and press Enter.

Private Message:
Use the format @recipient_name: your message to send a private message to a specific recipient.
List Connected Clients:

list active users:
Type /list to request a list of connected clients.

Exit the Chat:
Type /exit to gracefully disconnect from the chat.


