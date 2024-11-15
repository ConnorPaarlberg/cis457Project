import sys
import socket

class Server:
  def __init__(self, port_number):
    self.server_ip = '0.0.0.0'     # accept connections on all network interfaces
    self.port_number = port_number # the port number to use

    # create a socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    self.socket.bind((self.server_ip, self.port_number))

    # Listen for incoming connections
    self.socket.listen(5)
  
  def run(self):
    # Accept a connection
    client_socket, addr = self.socket.accept()
    print( 'Got connection from', addr)

    while(True):
        # Receive the message
        message = client_socket.recv(1024).decode()
        print('Received message:', message)

        # Send a response
        client_socket.send('Message received'.encode())

        if message == 'exit':
            # Close the connection
            client_socket.close()
            break

def main():
  port_number = int(sys.argv[1])

  server = Server(port_number)
  server.run()

if __name__ == '__main__':
  main()