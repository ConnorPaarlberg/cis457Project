import sys
import socket

class Client:
  def __init__(self, server_ip, port_number):
    self.server_ip = server_ip # the passed in IP address of the server
    self.port_number = port_number # the port number to connect to

    # create a socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    self.socket.connect((server_ip, port_number))
  
  def run(self):
    while(True):
      # prompt the user for input
      message = input("Enter a message: ")

      self.socket.send(message.encode()) # send the message

      # Receive a response
      response = self.socket.recv(1024)
      print('Received response:', response.decode())

      # exit the loop if the user types
      if message.lower() == 'exit':
        print("Closing connection")
        self.socket.close() # close the connection
        break

    
def main():
  # Get the server IP
  server_ip = sys.argv[1]
  port_number = int(sys.argv[2])

  client = Client(server_ip, port_number)
  client.run()

if __name__ == '__main__':
  main()