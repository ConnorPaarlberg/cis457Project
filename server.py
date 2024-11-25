import sys
import socket
import threading

from Battleship.Game import *
from Battleship.Battleship import *

class Server:
    def __init__(self, port_number, num_clients):
        self.server_ip = '0.0.0.0'     # Accept connections on all network interfaces
        self.port_number = port_number # The port number to use
        self.num_clients = num_clients # The desired number of clients to accept

        # Create a socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.socket.bind((self.server_ip, self.port_number))

        # Listen for incoming connections
        self.socket.listen(5)

        # A list of the client sockets
        self.clients = []

        # A dictionary to store each client's board
        self.boards = {}

        # Event for signaling threads to quit
        self.quit_event = threading.Event()

    def send_message(self, client_socket, message):
        client_socket.send(message.encode())

    def receive_message(self, client_socket):
        return client_socket.recv(1024).decode()

    def initialize_board(self, client_socket):
        """Send instructions to set up the board for a single client."""
        board = Board()
        self.boards[client_socket] = board

        self.send_message(client_socket, "Welcome to Battleship! Set up your board.")

        # Ask for ship placements
        ships = [
            (Square_SHIP.CARRIER, 5, "Where should the carrier go?"),
            (Square_SHIP.BATTLESHIP, 4, "Where should the battleship go?"),
            (Square_SHIP.CRUISER, 3, "Where should the cruiser go?"),
            (Square_SHIP.SUBMARINE, 3, "Where should the submarine go?"),
            (Square_SHIP.DESTROYER, 2, "Where should the destroyer go?"),
        ]

        for ship, length, message in ships:
            while True:
                self.send_message(client_socket, board.print_board_ships())
                self.send_message(client_socket, message)

                # Get coordinates and placement direction
                location = self.receive_message(client_socket).split()
                if len(location) != 2 or not all(c.isdigit() for c in location):
                    self.send_message(client_socket, "Invalid input. Try again.")
                    continue

                x, y = int(location[0]), int(location[1])
                self.send_message(client_socket, "Place vertically? (y/n)")
                vertical = self.receive_message(client_socket).lower() == 'y'

                if board.place_ship_on_board([x, y], ship, length, vertical):
                    break
                else:
                    self.send_message(client_socket, "Invalid placement. Try again.")

    def handle_client(self, client_socket, client_address):
        """Handle game interactions with a single client."""
        print(f"Connected to {client_address}")
        try:
            # Initialize the client's board
            self.initialize_board(client_socket)

            # Main game loop
            while not self.quit_event.is_set():
                # Send the current board state
                board = self.boards[client_socket]
                self.send_message(client_socket, board.print_board_state())

                # Ask the client where to attack
                self.send_message(client_socket, "Where should we attack? (Enter coordinates x y):")
                coordinates = self.receive_message(client_socket).split()

                if len(coordinates) != 2 or not all(c.isdigit() for c in coordinates):
                    self.send_message(client_socket, "Invalid input. Try again.")
                    continue

                x, y = int(coordinates[0]), int(coordinates[1])

                # Process the attack
                target_square = board.battlefield[x][y]
                if target_square.state == Square_State.NOT_TOUCHED:
                    target_square.square_attacked()
                    board.decrement_ship_health(target_square.ship)
                else:
                    self.send_message(client_socket, "This square has already been revealed!")

                # Check if the board is dead
                if board.state == Board_State.DEAD:
                    self.send_message(client_socket, "Game over! You lost!")
                    break

        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()
            print(f"Connection to {client_address} closed")

    def run(self):
      print("Server is running...")

      threads = []
      while len(self.clients) < self.num_clients:

        # Accept a connection
        client_socket, client_address = self.socket.accept()

        self.clients.append(client_socket)

        thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=False)

        threads.append(thread)

        thread.start() # start the thread
      
      for thread in threads:
        thread.join()

def main():
  if len(sys.argv) < 3:
    print("Error: must specify server port number & nuumber of clients")
    sys.exit(1)

  port_number = int(sys.argv[1]) # cast port number to an int
  num_clients = int(sys.argv[2]) # cast the number of clients to an int

  server = Server(port_number, num_clients)   # create the server
  try:
    server.run()  # run the server
  except KeyboardInterrupt:
      print("\nShutting down the server...")
  finally:
      server.socket.close()  # cleanup server socket
      print("Server socket closed.")

if __name__ == '__main__':
  main()