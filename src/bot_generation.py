import random
import csv
from src import utils

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def generate_ship(size, occupied):
    """
    Generate one valid ship of given size.
    Cheks that it does not touch other ships.
    """

    while True:
        direction = random.choice(['H', 'V'])

        if direction == 'H':
            x = random.randint(0, utils.BOARD_SIZE - 1)
            y = random.randint(0, utils.BOARD_SIZE - size)
            ship = [(x, y + i) for i in range(size)]

        else:
            x = random.randint(0, utils.BOARD_SIZE - size)
            y = random.randint(0, utils.BOARD_SIZE - 1)
            ship = [(x + i, y) for i in range(size)]

        if utils.is_valid_ship(ship, occupied):
            return ship

def generate_bot_ships():
    """
    Generate all ships for bot
    """
    ships = []
    occupied = set()

    for size in SHIP_SIZES:
        ship = generate_ship(size, occupied)
        ships.append(ship)

        for cell in ship:
            occupied.add(cell)

    return ships

def save_bot_ships(ships, filename):
    """
    Save generated bot ships to CSV.
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for ship in ships:
            writer.writerow(ship)

def run_bot_generation():
    """
    Main function: Generate and save bot ships.
    """
    ships = generate_bot_ships()
    save_bot_ships(ships, "data/bot_ships.csv")
    print("Bot ships generated and saved.")
