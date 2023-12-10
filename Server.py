import threading
import socket

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Bind the socket to a specific address and port
server.bind(('127.0.0.1', 65000))  

# Listen for incoming connections
server.listen()

# Lists to keep track of connected clients and their names
clients = []
names = []

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Function to kick a user from the chat
def kick_user(sender_name, kick_command):
    if kick_command.startswith('/kick'):
        _, kicked_name = kick_command.split(' ', 1)
        if kicked_name in names:
             # Kick the user by sending a message and closing the connection
            kicked_index = names.index(kicked_name)
            kicked_client = clients[kicked_index]
            kicked_client.send('You have been kicked from the chat room.'.encode('utf-8'))
            kicked_client.close()
        else:
            # Notify the sender that the user was not found
            sender_client = clients[names.index(sender_name)]
            sender_client.send(f'User {kicked_name} not found.'.encode('utf-8'))
        
# Function to handle each client's connection
def handle_client(client, address):
    try:
         # Receive the client's name
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)
         # Broadcast the new connection to all clients
        broadcast(f'{name} has connected to the chat room'.encode('utf-8'))

        while True:
            message = client.recv(1024)
            if not message:
                break

            if message.decode('utf-8').startswith('@'):
                # Private message format: "@recipient_name: message"
                recipient_name, private_message = message.decode('utf-8')[1:].split(':', 1)
                send_private_message(name, recipient_name, private_message)
            elif message.decode('utf-8') == '/list':
                # Send the list of clients to the requester
                client.send(', '.join(names).encode('utf-8'))
            elif message.decode('utf-8').startswith('/kick'):
                # Handle kicking a user
                kick_user(name, message.decode('utf-8'))
            elif message.decode('utf-8') == '/exit':
                # Handle client exit gracefully
                break
            else:
                # Broadcast the message to all clients
                broadcast(f'{name}: {message.decode("utf-8")}'.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        # Remove the client from the lists and broadcast their departure
        index = clients.index(client)
        clients.remove(client)
        name = names[index]
        broadcast(f'{name} has left the chat room!'.encode('utf-8'))
        names.remove(name)
        client.close()

# Function to send a private message to a specific user
def send_private_message(sender_name, recipient_name, private_message):
    # Find the recipient's client and send the private message
    if recipient_name in names:
        recipient_index = names.index(recipient_name)
        recipient_client = clients[recipient_index]
        # Send the private message to the recipient
        recipient_client.send(f'(Private from {sender_name}): {private_message}'.encode('utf-8'))
    else:
        sender_client = clients[names.index(sender_name)]
        # Notify the sender that the recipient was not found
        sender_client.send(f'Recipient {recipient_name} not found.'.encode('utf-8'))


# Function to continuously accept incoming connections
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        # Create a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

# Main entry point
if __name__ == "__main__":
    receive()

