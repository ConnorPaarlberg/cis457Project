from enum import Enum
from gui import Gui
from client import Client
import sys

class Board_State(Enum):
    ALIVE = 1
    DEAD = 2

class Square_State(Enum):
    NOT_TOUCHED = 3
    MISS = 4
    HIT = 5

class Ship:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.health = length
        
        self.start_coords = None
        self.end_coords = None
    
    def get_start_coords(self):
        return self.start_coords

    def get_end_coords(self):
        return self.end_coords

    def set_ship_coords(self, start_coords, end_coords):
        self.start_coords = start_coords
        self.end_coords = end_coords

    def hit(self):
        self.health -= 1

    def is_sunk(self):
        return self.health == 0

class Square:
    def __init__(self):
        self.state = Square_State.NOT_TOUCHED
        self.ship = None

    def add_ship_to_square(self, ship):
        self.ship = ship
    
    def square_attacked(self):
        if self.ship != None:
            self.state = Square_State.HIT
            self.ship.hit()
        else:
            self.state = Square_State.MISS
        return self.state

class Board:

    Ship_length_dict = {
        'carrier': 5,
        'battleship': 4,
        'cruiser': 3,
        'submarine': 3,
        'destroyer': 2
    }
    def __init__(self):

        # Initializing the state and squares of the board, 10 X 10 squares
        self.state = Board_State.ALIVE
        self.battlefield = [[Square() for x in range(10)] for y in range(10)]

        self.SHIPS = [Ship('carrier', 5),
                    Ship('battleship', 4),
                    Ship('cruiser', 3),
                    Ship('submarine', 3),
                    Ship('destroyer', 2)]

        self.number_of_ships_placed = 0

    def check_dead_board(self):
        total_ship_health = sum(ship.health for ship in self.SHIPS)
        if total_ship_health == 0:
            return True
        return False
    
    # Location is a tuple for the x and y axis [x,y]
    # SQUARE_SHIP is what ship we're placing
    # ship_length is how big the ship is
    # vertical_placement_bool - 0 if horizonal placement, 1 if vertical placement
    # Returns true if it was able to place a ship properly
    def place_ship_on_board(self, location, ship, ship_length, vertical_placement_bool):
        Invalid_Input = False
        ship_available = True
        row = location[0]
        column = location[1]

        if row < 0 or row > 9 or column < 0 or column > 9:
            Invalid_Input = True

        if vertical_placement_bool:
            if row + ship_length > 10:
                Invalid_Input = True
        else:
            if column + ship_length > 10:
                Invalid_Input = True

        if not Invalid_Input:
            if vertical_placement_bool:
                for i in range(ship_length):
                    if self.battlefield[row+i][column].ship != None:
                        ship_available = False
                if ship_available:
                    start_coords = (row, column)
                    end_coords = (row + ship_length - 1, column)
                    ship.set_ship_coords(start_coords, end_coords)

                    for i in range(ship_length):
                        self.battlefield[row+i][column].ship = ship
                        self.number_of_ships_placed += 1 

            else:
                for i in range(ship_length):
                    if self.battlefield[row][column+i].ship != None:
                        ship_available = False
                if ship_available:
                    start_coords = (row, column)
                    end_coords = (row, column + ship_length - 1)
                    ship.set_ship_coords(start_coords, end_coords)
                    for i in range(ship_length):
                        self.battlefield[row][column+i].ship = ship
                        self.number_of_ships_placed += 1
        if Invalid_Input or not ship_available:
            print(Invalid_Input)
            print(ship_available)
            return False
        return True
         

    def print_board_state(self):
        print_list = []

        for i in range (10):
            for j in range (10):
                print_list.append("|")
                current_square_state = self.battlefield[i][j].state
                if current_square_state == Square_State.NOT_TOUCHED:
                    print_list.append("-")
                elif current_square_state == Square_State.MISS:
                    print_list.append("X")
                else:
                    print_list.append("O")
            print_list.append("|")
            print_list.append("\n")

        print("".join(print_list))

    def print_board_ships(self):
        print_list = []
        print_column_list = ["  "]
        column_counter = 0

        for i in range(10):
            print_column_list.append(str(column_counter))
            print_column_list.append("  ")
            column_counter += 1
        print("".join(print_column_list))

        for i in range(10):
            print_list.append(str(i))
            for j in range(10):
                print_list.append("|")
                current_square_state = self.battlefield[i][j].ship
                if current_square_state == None:
                    print_list.append("--")
                else:
                    # use the first two letters of the ship name
                    print_list.append(current_square_state.name[:2].upper())
            print_list.append("|")
            print_list.append("\n")
        print("".join(print_list))

class BattleShip:
    def __init__(self, server_ip, port_number):
        self.board = Board() # the game board
        self.opponent_board = Board() # opponent board with less info
        # self.gui = Gui() # the gui for displaying the game
        self.client = Client(server_ip, port_number) # the client
        self.player_number = self.client.receive_message() # receive the player id

    def get_coordinate_input(self, message):
        if len(message) > 0:
            print(message)

        coordinates = input().split(' ')
        if len(coordinates) != 2:
            print("Invalid Input")
            return self.get_coordinate_input(message)

        try:
            xaxis = int(coordinates[0])
            yaxis = int(coordinates[1])
        except Exception:
            print("Invalid Input")

        else:
            if(xaxis > 9 or xaxis < 0 or yaxis > 9 or yaxis < 0):
                print("Coordinates not on board")
                return self.get_coordinate_input(message)
            else:
                return [xaxis,yaxis]
        
    def get_vertical_bool(self):
        print("Are you placing it vertically? (y/n)")
        vertical_bool = input()
        if vertical_bool == 'y':
            return True
        else: return False

    def build_board(self):
        for ship in self.SHIPS:
            self.board.print_board_ships()
            message = input("Where should the {ship.name.lower()} go?").split()
            location = self.get_coordinate_input(message)
            length = ship.length

            while self.board.place_ship_on_board(location, ship, length, self.get_vertical_bool()) == False:
                print("Invalid Placement, try again!")
                location = self.get_coordinate_input("")
        self.board.print_board_ships()
    
    """
    The purpose of this function is to attack their own board, then tell the other user what happened.
    
    This happens when a coordinate is sent by the other user during the other person's turn
    """
    def attack_board(self, target_board, target_coordinates):
        xaxis = target_coordinates[0]
        yaxis = target_coordinates[1]

        target_square = target_board.battlefield[xaxis][yaxis]

        if target_square.state == Square_State.NOT_TOUCHED:
            target_square.square_attacked()
            if self.board.check_dead_board() == True:
                print("The board is now dead")
                self.state = Board_State.DEAD

        else:
            print("This square has already been revealed!")

        # the json that will be sent containing all relevant information
        attack_info = {
            #TODO: replace this with board-state of copy board
            "board_state": self.board.state.name, # add the board state to the attack info
            "attack_status": target_square.state.name, # the status of the attack (hit/miss)
            "coordinate_of_attack": target_coordinates,
            "ship_info": {
                "name": target_square.ship.name,
                "start_coords": target_square.ship.get_start_coords(),
                "end_coords": target_square.ship.get_end_coords(),
                "is_sunk": target_square.ship.is_sunk()
            } if target_square.ship else None, # only ship info if there is actually a ship on that square (could be none)
        }
        return attack_info
    

    """
    Check if the spot your targetting is valid based on your copy of the opponent's board
    """
    def is_valid_attack_coordinates(self, coordinates):
        xaxis = coordinates[0]
        yaxis = coordinates[1]
        
        # the json that will be sent containing all relevant information
        attack_info = {
            #TODO: replace this with board-state of copy board
            "board_state": self.board.state.name, # add the board state to the attack info
            "attack_status": target_square.state.name, # the status of the attack (hit/miss)
            "coordinate_of_attack": target_coordinates,
            "ship_info": {
                "name": target_square.ship.name,
                "start_coords": target_square.ship.get_start_coords(),
                "end_coords": target_square.ship.get_end_coords(),
                "is_sunk": target_square.ship.is_sunk()
            } if target_square.ship else None, # only ship info if there is actually a ship on that square (could be none)
        }
        return attack_info
    

    """
    Check if the spot your targetting is valid based on your copy of the opponent's board
    """
    def is_valid_attack_coordinates(self, coordinates):
        xaxis = coordinates[0]
        yaxis = coordinates[1]
        
        # check if the coordinates are within the valid range
        if xaxis < 0 or xaxis > 9 or yaxis < 0 or yaxis > 9:
            return False

        # check if the square has already been attacked
        target_square = self.opponent_board.battlefield[xaxis][yaxis]
        if target_square.state != Square_State.NOT_TOUCHED:
            return False

        return True
    
    """
    Function that takes in the attack_info JSON and adjusts the player's boards
    """
    def adjust_board_after_attack(self, attack_info):

        # Set variables for the opponent square
        coordinate_xaxis = attack_info["coordinate_of_attack"][0]
        coordinate_yaxis = attack_info["coordinate_of_attack"][1]
        opponent_square = self.opponent_board.battlefield[coordinate_xaxis][coordinate_yaxis]

        # First we adjust our opponent_board's coordinate to check if it hit or not
        given_square_state_info = attack_info["attack_status"]

        if given_square_state_info == "HIT":
            opponent_square.state == Square_State.HIT
        else:
            opponent_square.state == Square_State.MISS

        # Second we only reveal the ship, if we know that we have sunk it
        ship_info = attack_info["ship_info"]["name"]

        # if ship_info exists
        if ship_info:

            # If the ship we hit has sunk, we mark it down on our board
            if ship_info["is_sunk"]:
                coordinate = attack_info["coordinate_of_attack"]
                ship_name = attack_info["ship_info"]["name"]
                ship_length = Board.Ship_length_dict[ship_name]

                ship = Ship(ship_name,ship_length)

                vert_bool = attack_info["end_coords"][0] > attack_info["start_coords"][0]
                self.opponent_board.place_ship_on_board(coordinate,ship,ship_length,vert_bool)

        if attack_info["board_state"] == "DEAD":
            print("YOU WIN") 
            #TODO Leaves the connection or play again, not sure yet


        
    
    def play(self):
        # self.gui.run()

        self.build_board() # build the game board
        game_turn = 1 # player 1 always has first turn

        # core game loop
        while self.board.state == Board_State.ALIVE:
            if self.player_number == game_turn:
                # loop until a valid coordinate has been entered on the enemy's board
                coordinates = self.get_coordinate_input('Enter a location to attack: ')
                while not self.is_valid_attack_coordinates(coordinates):
                    print('Invalid coordinates')
                    coordinates = self.get_coordinate_input('Enter a location to attack: ')

                self.client.send_message(coordinates) # send the coordinates to the server

                attack_response = self.client.receive_message() # receive the result of the attack (JSON)
                print(attack_response) # print the attack response TODO delete me later!

                self.adjust_board_after_attack(attack_response)

                game_turn = (game_turn % 2) + 1 # switch roles
            else:
                print("Waiting for player to attack")
                response = self.client.receive_message() # receive the desired spot to hit from the server
                print(response) # print the desired coordinates to attack TODO delete me later!

                attack_info = self.attack_board(self.board, response) # attack the board TODO make sure this method attacks enemy

                print(attack_info) # print out the attack info TODO delete me later!
                self.client.send_message(attack_info) # send the attack info to the server



                game_turn = (game_turn % 2) + 1 # switch roles

def main():
  if len(sys.argv) < 3:
    print("Error: must specify server IP and port number")
    sys.exit(1)

  server_ip = sys.argv[1] # get the server IP
  port_number = int(sys.argv[2]) # get the port number

  battleship = BattleShip(server_ip, port_number)
  battleship.play()

if __name__ == "__main__":
    main()
