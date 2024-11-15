import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = socket.gethostname()

# Connect to the server
client_socket.connect((host, 12345))

# Send a message
message = 'Hello, server!'
client_socket.send(message.encode())

# Receive a response
response = client_socket.recv(1024)
print('Received response:', response.decode())

# Close the connection
client_socket.close()