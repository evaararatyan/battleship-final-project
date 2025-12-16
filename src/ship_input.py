import csv
from src import utils

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def get_player_input():
    """
    Ask player to enter ship coordinates.
    """
    ships = []

    print("Enter ship coordinates.")
    print("Example for size 3: 0,0 0,1 0,2")

    for size in SHIP_SIZES:
        while True:
            raw = input(f"Enter ship of size {size}: ")
            parts = raw.split()

            if len(parts) != size:
                print("Wrong number of cells.")
                continue

            ship = []
            valid = True

            for part in parts:
                try:
                    x, y = map(int, part.split(","))
                    if not utils.is_inside_board(x, y):
                        valid = False
                    ship.append((x, y))
                except:
                    valid = False

            if not valid:
                print("Invalid coordinates.")
                continue

            if not utils.is_straight_line(ship):
                print("Ship must be in a straight line.")
                continue

            if not utils.is_consecutive(ship):
                print("Ship cells must be consecutive.")
                continue

            ships.append(ship)
            break

    return ships


def validate_ships(ships):
    """
    Check that ships do not touch each other.
    """
    occupied = set()

    for ship in ships:
        if not utils.is_valid_ship(ship, occupied):
            return False

        for cell in ship:
            occupied.add(cell)

    return True


def save_ships_to_csv(ships, filename):
    """
    Save ships to CSV file.
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for ship in ships:
            writer.writerow(ship)


def run_ship_input():
    """
    Main function for ship input.
    """
    while True:
        ships = get_player_input()

        if validate_ships(ships):
            save_ships_to_csv(ships, "data/player_ships.csv")
            print("Ships saved successfully.")
            break
        else:
            print("Invalid ship placement. Try again.")