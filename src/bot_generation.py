import csv
import random
from src import utils

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def generate_bot_ships():
    '''
    Generate a list of ships for the bot randomly
    Each ship is a list of coordinates
    '''
    ships = []
    occupied = set()

    for size in SHIP_SIZES:
        while True:
            horizontal = random.choice([True, False])
            if horizontal:
                x = random.randint(0, utils.BOARD_SIZE - 1)
                y = random.randint(0, utils.BOARD_SIZE - size)
                ship = [(x, y + i) for i in range(size)]
            else:
                x = random.randint(0, utils.BOARD_SIZE - size)
                y = random.randint(0, utils.BOARD_SIZE - 1)
                ship = [(x + i, y) for i in range(size)]

            if utils.is_valid_ship(ship, occupied):
                ships.append(ship)
                for c in ship:
                    occupied.add(c)
                break

    return ships

def save_bot_ships_to_csv(ships, filename="data/bot_ships.csv"):
    '''
    Save the generated bot ships to a CSV file
    Each row in the CSV represents one ship 
    '''

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        for ship in ships:
            flat = [coord for pair in ship for coord in pair]
            writer.writerow(flat)

def run_bot_generation():
    '''
    Generate bot ships and save them to CSV.
    Print a confirmation message.
    '''

    ships = generate_bot_ships()
    save_bot_ships_to_csv(ships)
    print("Bot ships generated and saved successfully!")

if __name__ == "__main__":
    run_bot_generation()
