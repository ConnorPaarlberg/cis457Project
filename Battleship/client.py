import socket
import struct
import json

class Client:
  def __init__(self, server_ip, port_number):
    self.server_ip = server_ip # the passed in IP address of the server
    self.port_number = port_number # the port number to connect to

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
    self.socket.connect((server_ip, port_number))  # connect to the server
  
  def send_message(self, data):
    message = json.dumps(data).encode('utf-8') # encode the message into json
    length = struct.pack('!I', len(message))   # pack the length into a big-endian, unsigned integer

    self.socket.sendall(length + message) # send the length and message

  def receive_message(self):
    length_bytes = self.socket.recv(4) # read 4 bytes for the length
    length = struct.unpack('!I', length_bytes)[0] # unpack the length

    message = self.socket.recv(length) # read the appropriate number of bytes

    message = json.loads(message.decode('utf-8')) # decode the message to a string and convert it back to a Python object

    return message # return the received message