from Battleship import *

def convert_coordinate_input(input):
    coordinates = input.split(',')
    return [int(coordinates[0]), int(coordinates[1])]


Current_Board = Board()

print("Where should the carrier go?")
carrier_location = convert_coordinate_input(input())
Current_Board.place_ship_on_board(carrier_location,Square_SHIP.CARRIER, 5, bool(input("Are you placing it vertically? (True/False) ")))



print("Where should the battleship go?")
battleship_location = convert_coordinate_input(input())
Current_Board.place_ship_on_board(carrier_location,Square_SHIP.BATTLESHIP, 5, bool(input("Are you placing it vertically? (True/False) ")))
print("Where should the cruiser go?")
cruiser_location = convert_coordinate_input(input())
Current_Board.place_ship_on_board(carrier_location,Square_SHIP.CRUISER, 5, bool(input("Are you placing it vertically? (True/False) ")))
print("Where should the submarine go?")
submarine_location = convert_coordinate_input(input())
Current_Board.place_ship_on_board(carrier_location,Square_SHIP.SUBMARINE, 5, bool(input("Are you placing it vertically? (True/False) ")))
print("Where should the destroyer go?")
destroyer_location = convert_coordinate_input(input())
Current_Board.place_ship_on_board(carrier_location,Square_SHIP.DESTROYER, 5, bool(input("Are you placing it vertically? (True/False) ")))

Current_Board.print_board_ships()
