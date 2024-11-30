import sys
import socket
import struct
import threading
import json

class Server:
  player_id = 1
  def __init__(self, port_number, num_clients):
    self.server_ip = '0.0.0.0'     # accept connections on all network interfaces
    self.port_number = port_number # the port number to use
    self.num_clients = num_clients # the desired number of clients to accept

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket
    self.socket.bind((self.server_ip, self.port_number)) # bind the socket to the port
    self.socket.listen(5) # listen for incoming connections

    self.clients = [] # a list of the client sockets
    self.quit_event = threading.Event() # event for signaling threads to quit

  def handle_client(self, client_socket, client_address):
    print(f"Connected to {client_address}")

    self.send_message(client_socket, Server.player_id) # send the player ID to the client
    Server.player_id += 1 # increment the player ID

    while not self.quit_event.is_set():
      # receive the message
      message = self.receive_message(client_socket)

      # send the message to the other client
      for connected_socket in self.clients:
        if client_socket != connected_socket:
          self.send_message(connected_socket, message)

      if 'board_state' in message and message['board_state'] == 'DEAD':
        break

    # self.quit_event.set() # signal to quit
    # self.clients.remove(client_socket)
    # client_socket.close() # close the connection
    # print(f"Connection to {client_address} closed")
  
  def send_message(self, client_socket, data):
    message = json.dumps(data).encode('utf-8') # encode the message into json
    length = struct.pack('!I', len(message))   # pack the length into a big-endian, unsigned integer

    client_socket.sendall(length + message) # send the length and message

  def receive_message(self, client_socket):
    length_bytes = client_socket.recv(4) # read 4 bytes for the length
    length = struct.unpack('!I', length_bytes)[0] # unpack the length

    message = client_socket.recv(length) # read the appropriate number of bytes

    message = json.loads(message.decode('utf-8')) # decode the message to a string and convert it back to a Python object

    return message # return the response

  def run(self):
    print("Server is running...")

    threads = [] # for joining the threads later
    while len(self.clients) < self.num_clients:
      client_socket, client_address = self.socket.accept() # accept a connection

      self.clients.append(client_socket) # add this client to the list

      # create a new thread
      thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=False)

      threads.append(thread) # add this thread to the list
      thread.start() # start the thread

    for thread in threads:
      thread.join() # join each thread (good practice)

def main():
  if len(sys.argv) < 3:
    print("Error: must specify server port number & number of clients")
    sys.exit(1)

  port_number = int(sys.argv[1]) # cast port number to an int
  num_clients = 2 # only want 2 clients for our battleship game
  server = Server(port_number, num_clients) # create the server
  server.run() # run the server

if __name__ == '__main__':
  main()