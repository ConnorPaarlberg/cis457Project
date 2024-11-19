from enum import Enum

class Board_State(Enum):
    ALIVE = 1
    DEAD = 2

class Square_State(Enum):
    NOT_TOUCHED = 3
    MISS = 4
    HIT = 5

class Square_SHIP(Enum):
    NOTHING = 6
    CARRIER = 7
    BATTLESHIP = 8
    CRUISER = 9
    SUBMARINE = 10
    DESTROYER = 11

class Square:
    def __init__(self):
        self.state = Square_State.NOT_TOUCHED
        self.ship = Square_SHIP.NOTHING

    def add_ship_to_square(self,Square_SHIP):
        self.ship = Square_SHIP

class Board:
    def __init__(self):

        # Initializing the state and squares of the board, 10 X 10 squares
        self.state = Board_State.ALIVE
        self.battlefield = [[Square() for x in range(10)] for y in range(10)]
        # self.player_name = 

        # Health points for each of the ships on the board
        # If 0, they're dead
        self.carrier_hp = 5
        self.battleship_hp = 4
        self.cruiser_hp = 3
        self.submarine_hp = 3
        self.destroyer_hp = 2

        self.number_of_ships_placed = 0

    def check_dead_board(self):
        sum = self.carrier_hp + self.battleship_hp + self.cruiser_hp + self.submarine_hp + self.destroyer_hp
        if sum == 0:
            return True
        return False
    
    # Location is a tuple for the x and y axis [x,y]
    # SQUARE_SHIP is what ship we're placing
    # ship_length is how big the ship is
    # vertical_placement_bool - 0 if horizonal placement, 1 if vertical placement
    def place_ship_on_board(self, location, ship, ship_length, vertical_placement_bool):
        Invalid_Input = False

        Xaxis = location[0]
        Yaxis = location[1]

        if Xaxis < 0 or Xaxis > 9 or Yaxis < 0 or Yaxis > 9:
            Invalid_Input = True

        if Xaxis + ship_length > 9 or Yaxis + ship_length > 9:
            Invalid_Input = True

        if not Invalid_Input:
            ship_available = True
            if vertical_placement_bool:
                for i in range(ship_length):
                    if self.battlefield[Xaxis][Yaxis+i].ship != Square_SHIP.NOTHING:
                        ship_available = False
                if ship_available:
                    for i in range(ship_length):
                        self.battlefield[Xaxis][Yaxis+i].ship = ship
                        self.number_of_ships_placed += 1 

            else:
                for i in range(ship_length):
                    if self.battlefield[Xaxis+i][Yaxis].ship != Square_SHIP.NOTHING:
                        ship_available = False
                if ship_available:
                    for i in range(ship_length):
                        self.battlefield[Xaxis+i][Yaxis].ship = ship
                        self.number_of_ships_placed += 1        
