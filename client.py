import socket
import sys

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
server_ip = sys.argv[1]

# Connect to the server
client_socket.connect((server_ip, 12345))

print("Connected to the server. Type your messages below. (exit to quit)\n")


while True:
    # Prompt the user for input
    message = input("Enter a message: ")
    
    # Exit the loop if the user types 'exit'
    if message.lower() == 'exit':
        print("Closing connection.")
        break

    # Send the message to the server
    client_socket.send(message.encode())

    # Receive a response from the server
    response = client_socket.recv(1024)
    print('Received response:', response.decode())