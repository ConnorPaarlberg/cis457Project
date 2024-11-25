from Battleship import *

def get_coordinate_input(message):
    if len(message) > 0:
        print(message)

    coordinates = input().split(' ')
    if len(coordinates) != 2:
        print("Invalid Input")
        get_coordinate_input(message)

    try:
        xaxis = int(coordinates[0])
        yaxis = int(coordinates[1])
    except Exception:
        print("Invalid Input")

    else:
        if(xaxis > 9 or xaxis < 0 or yaxis > 9 or yaxis < 0):
            print("Coordinates not on board")
            get_coordinate_input(message)
        else:
            return [xaxis,yaxis]
    
def get_vertical_bool():
    print("Are you placing it vertically? (y/n)")
    vertical_bool = input()
    if vertical_bool == 'y':
        return True
    else: return False

def build_board(board,ship,length,message):
    location = get_coordinate_input(message)

    while board.place_ship_on_board(location, ship, length, get_vertical_bool()) == False:
        print("Invalid Placement, try again!")
        location = get_coordinate_input("")

    board.print_board_ships()
 
def attack_board(target_board):
    #TODO Check for valid location
    coordinates = get_coordinate_input("Where should we attack?")
    xaxis = coordinates[0]
    yaxis = coordinates[1]
    target_square = target_board.battlefield[xaxis][yaxis]

    if target_square.state == Square_State.NOT_TOUCHED:
        target_square.square_attacked()
        target_board.decrement_ship_health(target_square.ship)

    else:
        print("This square has already been revealed!")

def main():

    Current_Board = Board()

    Current_Board.print_board_ships()

    build_board(Current_Board, Square_SHIP.CARRIER, 5, "Where should the carrier go?")

    build_board(Current_Board, Square_SHIP.BATTLESHIP, 4, "Where should the battleship go?")

    build_board(Current_Board, Square_SHIP.CRUISER, 3, "Where should the cruiser go?")

    build_board(Current_Board, Square_SHIP.SUBMARINE, 3, "Where should the submarine go?")

    build_board(Current_Board, Square_SHIP.DESTROYER, 2, "Where should the destroyer go?")


    while Current_Board.state == Board_State.ALIVE: 
        attack_board(Current_Board)
        Current_Board.print_board_ships()
        Current_Board.print_board_state()

if __name__ == "__main__":
    main()