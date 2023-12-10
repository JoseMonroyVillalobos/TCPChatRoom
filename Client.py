import threading
import socket

# Get the user's name
name = input('Enter name: ')

# Create a socket object and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65000))

# Function to receive messages from the server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f'Error receiving message: {e}')
            client.close()
            exit(0)

# Function to send messages to the server
def client_send():
    # Send the name to the server after connecting
    client.send(name.encode('utf-8'))

    while True:
        # Get user input for messages
        message = input("")
        if message.startswith('@'):
            # Private message format: "@recipient_name: message"
            client.send(message.encode('utf-8'))
        elif message.startswith('/list'):
            # Request the list of clients from the server
            client.send('/list'.encode('utf-8'))
        elif message.startswith('/kick'):
            # Kick a user
            client.send(message.encode('utf-8'))
        elif message == '/exit':
            # Gracefully close the connection
            client.send('/exit'.encode('utf-8'))
            client.close()
            exit(0)
        else:
            # Send the message to the server
            client.send(f'{message}'.encode('utf-8'))

# Create threads for receiving and sending messages
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
