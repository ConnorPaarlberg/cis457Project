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
    # Serialize the message (JSON) to a string
    message_json = json.dumps(message)
    # Encode the JSON string as bytes
    message_bytes = message_json.encode('utf-8')
    # Send the length of the message first (so the receiver knows how much data to expect)
    message_length = len(message_bytes)
    self.socket.send(struct.pack('!I', message_length))
    # Send encoded json
    self.socket.send(message_bytes)
  
  def receive_message(self, receiving_player_id=False):
    # returns player id
    if receiving_player_id:
        response = self.socket.recv(4)
        response = struct.unpack('!i', response)[0]
    # returns json data sent by other client
    else:
        # Receive the message length
        response_length_bytes = self.socket.recv(4)
        response_length = struct.unpack('!I', response_length_bytes)[0]

        # Receive the full json data before returning
        response_bytes = b""
        while len(response_bytes) < response_length:
            chunk = self.socket.recv(response_length - len(response_bytes))
            response_bytes += chunk
        
        # Decode and parse the JSON
        response_json = response_bytes.decode('utf-8')
        response = json.loads(response_json)

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