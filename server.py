import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = '0.0.0.0'

# Reserve a port for your service.
port = 12345

# Bind the socket to the port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

while True:
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)

        try: 
            while True:
                # Receive the message
                message = client_socket.recv(1024)
                print('Received message:', message.decode())

                # Send a response
                client_socket.send('Message received'.encode())
        finally:
            # Close the connection
            client_socket.close()