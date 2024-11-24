import sys
import socket
import select
import threading

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
  
  def send_messages(self):
    while not self.quit_event.is_set():
      # Use select to wait for user input with a timeout so that quit_event is checked regularly
      readable, _, _ = select.select([sys.stdin], [], [], 1)  # 1-second timeout

      if readable:
        message = input()

        self.socket.send(message.encode())  # send the message

        if message.lower() == "exit":
            self.quit_event.set()  # signal to quit
            break
  
  def receive_messages(self):
    while not self.quit_event.is_set():
      # Use select to wait for data with a timeout so that the quit_event is checked regularly
      readable, _, _ = select.select([self.socket], [], [], 1)  # 1-second timeout

      if readable:
        response = self.socket.recv(1024).decode()
        if response == '':
            continue

        print(response)

        if response.lower() == "exit":
            self.quit_event.set()  # signal to quit
            break

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