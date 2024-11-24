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
    
    def square_attacked(self):
        if self.ship != Square_SHIP.NOTHING:
            self.state = Square_State.HIT
            print("You hit a ship!")
            return True
        else:
            self.state = Square_State.MISS
            print("You missed!")
            return False

class Board:
    def __init__(self):

        # Initializing the state and squares of the board, 10 X 10 squares
        self.state = Board_State.ALIVE
        self.battlefield = [[Square() for x in range(10)] for y in range(10)]
        # self.player_name = 

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

