import csv
from src import utils

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def get_player_input():
    """
    Ask player to enter ship coordinates.
    Returns a list of ships, where each ship is a list of (x, y).
    """
    ships = []

    print("Enter ships coordinates.")
    print("Format example for ship of size 3: 0,0 0,1 0,2")

    for size in SHIP_SIZES:
        while True:
            raw = input(f"Enter ship of size {size}: ")
            coords = raw.split()

            if len(coords) != size:
                print("Wrong number of cells.")
                continue

            ship = []
            valid = True

            for c in coords:
                try:
                    x, y = map(int, c.split(","))
                    if not utils.is_inside_board(x, y):
                        valid = False
                    ship.append((x, y))
                except:
                    valid = False

            if not valid:
                print("Invalid coordinates.")
                continue

            ships.append(ship)
            break

    return ships


def validate_ships(ships):
    """
    Check that ships do not touch and are placed correctly.
    Returns True if valid, False otherwise.
    """
    board = utils.create_empty_board()

    for ship in ships:
        if not utils.is_valid_ship(ship):
            return False

        for x, y in ship:
            if board[x][y] == 1:
                return False

            board[x][y] = 1

            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if utils.is_inside_board(nx, ny):
                        if board[nx][ny] == 1 and (nx, ny) not in ship:
                            return False

    return True


def save_ships_to_csv(ships, filename):
    """
    Save ship coordinates to CSV file.
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for ship in ships:
            writer.writerow(ship)


def run_ship_input():
    """
    Main function for player ship input.
    """
    while True:
        ships = get_player_input()

        if validate_ships(ships):
            save_ships_to_csv(ships, "data/player_ships.csv")
            print("Ships saved successfully.")
            break
        else:
            print("Ships placement is invalid. Try again.")
