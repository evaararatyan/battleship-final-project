import csv
from src import utils

# Размеры кораблей
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def get_player_input():
    """
    Ask player to enter ship coordinates for all ships.
    Returns list of ships, each ship = list of (x,y) tuples.
    """
    ships = []
    print("Enter ship coordinates.")
    print("Format example for size 3: 0 0 0 1 0 2 (space-separated x y pairs)")

    for size in SHIP_SIZES:
        while True:
            raw = input(f"Enter ship of size {size}: ")
            parts = raw.split()

            if len(parts) != size * 2:
                print(f"Wrong number of coordinates! You need {size*2} numbers.")
                continue

            ship = []
            valid = True
            for i in range(0, len(parts), 2):
                try:
                    x = int(parts[i])
                    y = int(parts[i+1])
                    if not utils.is_inside_board(x, y):
                        valid = False
                    ship.append((x, y))
                except:
                    valid = False

            if not valid:
                print("Invalid coordinates. Try again.")
                continue

            # Проверка, что корабль не касается других
            occupied = set(cell for s in ships for cell in s)
            if not utils.is_valid_ship(ship, occupied):
                print("Ship cannot touch other ships. Try again.")
                continue

            ships.append(ship)
            break

    return ships


def save_ships_to_csv(ships, filename="data/player_ships.csv"):
    """
    Save list of ships to CSV file.
    Each ship is one row: x1,y1,x2,y2,...
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for ship in ships:
            flat = [coord for pair in ship for coord in pair]
            writer.writerow(flat)


def run_ship_input():
    """
    Main function to run ship input process.
    """
    ships = get_player_input()
    save_ships_to_csv(ships)
    print("Ships saved successfully!")

# Для тестирования напрямую:
if __name__ == "__main__":
    run_ship_input()
