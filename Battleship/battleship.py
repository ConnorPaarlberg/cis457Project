from enum import Enum
from gui import Gui
from client import Client
import sys
import json

class Board_State(Enum):
    ALIVE = 1
    DEAD = 2

class Square_State(Enum):
    NOT_TOUCHED = 3
    MISS = 4
    HIT = 5

class Square_SHIP(Enum):
    NOTHING = 0
    CARRIER = 5
    BATTLESHIP = 4
    CRUISER = 3
    SUBMARINE = 3
    DESTROYER = 2

class Square:
    def __init__(self):
        self.state = Square_State.NOT_TOUCHED
        self.ship = Square_SHIP.NOTHING

    def add_ship_to_square(self,Square_SHIP):
        self.ship = Square_SHIP
    
    def square_attacked(self):
        if self.ship != Square_SHIP.NOTHING:
            self.state = Square_State.HIT
        else:
            self.state = Square_State.MISS
        return self.state

class Board:
    def __init__(self):

        # Initializing the state and squares of the board, 10 X 10 squares
        self.state = Board_State.ALIVE
        self.battlefield = [[Square() for x in range(10)] for y in range(10)]

        self.number_of_ships_placed = 0

        # Health points for each of the ships on the board
        # If 0, they're dead
        self.carrier_hp = 5
        self.battleship_hp = 4
        self.cruiser_hp = 3
        self.submarine_hp = 3
        self.destroyer_hp = 2

    def check_dead_board(self):
        sum = self.carrier_hp + self.battleship_hp + self.cruiser_hp + self.submarine_hp + self.destroyer_hp
        if sum == 0:
            return True
        return False
    
    def decrement_ship_health(self, hurt_ship):
        match hurt_ship:
            case Square_SHIP.CARRIER:
                self.carrier_hp-=1
            case Square_SHIP.BATTLESHIP:
                self.battleship_hp-=1
            case Square_SHIP.CRUISER:
                self.cruiser_hp -=1
            case Square_SHIP.SUBMARINE:
                self.submarine_hp -=1
            case Square_SHIP.DESTROYER:
                self.destroyer_hp -=1
        if self.check_dead_board() == True:
            print("This board is now dead")
            self.state = Board_State.DEAD
    
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
                    if self.battlefield[row+i][column].ship != Square_SHIP.NOTHING:
                        ship_available = False
                if ship_available:
                    for i in range(ship_length):
                        self.battlefield[row+i][column].ship = ship
                        self.number_of_ships_placed += 1 

            else:
                for i in range(ship_length):
                    if self.battlefield[row][column+i].ship != Square_SHIP.NOTHING:
                        ship_available = False
                if ship_available:
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
        row_counter = 0
        column_counter = 0

        for i in range(10):
            print_column_list.append(str(column_counter))
            print_column_list.append("  ")
            column_counter+=1
        print("".join(print_column_list))


        for i in range (10):
            print_list.append(str(row_counter))
            for j in range (10):
                print_list.append("|")
                current_square_state = self.battlefield[i][j].ship
                if current_square_state == Square_SHIP.NOTHING:
                    print_list.append("--")
                elif current_square_state == Square_SHIP.CARRIER:
                    print_list.append("CA")
                elif current_square_state == Square_SHIP.BATTLESHIP:
                    print_list.append("BA")

                elif current_square_state == Square_SHIP.CRUISER:
                    print_list.append("CR")
                elif current_square_state == Square_SHIP.SUBMARINE:
                    print_list.append("SU")
                else:
                    print_list.append("DE")
            row_counter +=1
            print_list.append("|")
            print_list.append("\n")
        print("".join(print_list))

class BattleShip:
    def __init__(self, server_ip, port_number):
        self.board = Board() # the game board
        # self.gui = Gui() # the gui for displaying the game
        self.client = Client(server_ip, port_number) # the client
        self.player_number = self.client.receive_message(receiving_player_id=True) # receive the player number

        self.ships = [Square_SHIP.CARRIER, Square_SHIP.BATTLESHIP, Square_SHIP.CRUISER, Square_SHIP.SUBMARINE, 
        Square_SHIP.DESTROYER]
    
    def play(self):
        # self.gui.run()

        self.build_board() # build the game board
        game_turn = 1 # player 1 always has first turn

        # core game loop
        while self.board.state == Board_State.ALIVE:
            if self.player_number == game_turn:
                coordinates = input("Enter a target to attack: ").split()
                while len(coordinates) < 2:
                    coordinates = input("Invalid input. Enter a target to attack: ").split()

                # TODO: needs to be altered so that the json data is reflecting the results 
                # of the opponents board, not their own board. Currently, it shows accurate
                # HIT/MISS and battleship for own board
                coordinates = [int(coord) for coord in coordinates]
                json_message = {
                    "player_id": self.player_number,
                    "coordinates": coordinates,
                    "square state": str(self.attack_board(self.board, coordinates)),
                    "square ship": str(self.board.battlefield[coordinates[0]][coordinates[1]].ship),
                    "board state": str(self.board.state)
                }
                print("Your Move Information: \n", json_message)
                self.client.send_message(json_message)
                game_turn = (game_turn % 2) + 1
            else:
                print("Waiting for player to attack")
                response = self.client.receive_message()
                print("Opponent Move Information: \n", response)

                game_turn = (game_turn % 2) + 1

    def get_coordinate_input(self, message):
        if len(message) > 0:
            print(message)

        coordinates = input().split(' ')
        if len(coordinates) != 2:
            print("Invalid Input")
            self.get_coordinate_input(message)

        try:
            xaxis = int(coordinates[0])
            yaxis = int(coordinates[1])
        except Exception:
            print("Invalid Input")

        else:
            if(xaxis > 9 or xaxis < 0 or yaxis > 9 or yaxis < 0):
                print("Coordinates not on board")
                self.get_coordinate_input(message)
            else:
                return [xaxis,yaxis]
        
    def get_vertical_bool(self):
        print("Are you placing it vertically? (y/n)")
        vertical_bool = input()
        if vertical_bool == 'y':
            return True
        else: return False

    def build_board(self):
        for ship in self.ships:
            self.board.print_board_ships()
            message = f"Where should the {ship.name.lower()} go?"
            location = self.get_coordinate_input(message)
            length = ship.value

            while self.board.place_ship_on_board(location, ship, length, self.get_vertical_bool()) == False:
                print("Invalid Placement, try again!")
                location = self.get_coordinate_input("")
        self.board.print_board_ships()
    
    def attack_board(self, target_board, target_coordinates):
        #TODO Check for valid location
        xaxis = target_coordinates[0]
        yaxis = target_coordinates[1]

        target_square = target_board.battlefield[xaxis][yaxis]

        if target_square.state == Square_State.NOT_TOUCHED:
            target_square.square_attacked()
            target_board.decrement_ship_health(target_square.ship)

        else:
            print("This square has already been revealed!")
        
        return target_square.state

def main():
  # Get the server IP
  server_ip = sys.argv[1]
  port_number = int(sys.argv[2])

  battleship = BattleShip(server_ip, port_number)
  battleship.play()

if __name__ == "__main__":
    main()