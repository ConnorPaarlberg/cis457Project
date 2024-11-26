import sys
import socket
import select
import struct
import threading
import json

class Client:
  def __init__(self, server_ip, port_number):
    self.server_ip = server_ip # the passed in IP address of the server
    self.port_number = port_number # the port number to connect to

    # create a socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    self.socket.connect((server_ip, port_number))

    # event for signaling threads to quit
    self.quit_event = threading.Event() 
  
  def send_message(self, message):
    message = struct.pack('!ii', int(message[0]), int(message[1]))
    self.socket.send(message) # send the player id and turn to the client
  
  def receive_message(self, receiving_player_id=False):
    if receiving_player_id:
      response = self.socket.recv(4)
      response = struct.unpack('!i', response)[0]
    else:
      response = self.socket.recv(8)
      response = struct.unpack('!ii', response)
    return response

  def run(self):
    sender_thread = threading.Thread(target=self.send_messages, daemon=False) # create the sender thread

    receiver_thread = threading.Thread(target=self.receive_messages, daemon=False) # create the receiver thread

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()
    receiver_thread.join()

    self.socket.close() # close the connection

    
def main():
  # Get the server IP
  server_ip = sys.argv[1]
  port_number = int(sys.argv[2])

  client = Client(server_ip, port_number)
  client.run()

if __name__ == '__main__':
  main()