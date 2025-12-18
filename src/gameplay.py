import csv
import random
from src.utils import create_empty_board, print_board, is_inside_board, get_neighbors

def run_game():
    """
    Run the Battleship game loop.
    Shows both boards for testing: player's and bot's (only hits/misses).
    """

    def load_ships(filename):
        """
        Load ships from CSV file.
        Each row = one ship: x1,y1,x2,y2..
        Returns list of ships (list of coordinate tuples).
        """
        ships = []
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                ship = [(int(row[i]), int(row[i+1])) for i in range(0, len(row), 2)]
                ships.append(ship)
        return ships

    def check_hit(shot, ships):
        """
        Check if a shot hits any ship.
        Returns:
            hit (bool) - True if hit
            ship (list) - the ship that was hit (or None if no hit)
        """
        for ship in ships:
            if shot in ship:
                ship.remove(shot)
                return True, ship
        return False, None

    # -creation of empty board-
    player_board = create_empty_board()
    bot_board = create_empty_board()

    # -importing ships from csv--
    player_ships = load_ships("data/player_ships.csv")
    bot_ships = load_ships("data/bot_ships.csv")

    # === NEW: place player ships on board ===
    for ship in player_ships:
        for x, y in ship:
            player_board[x][y] = "S"

    # -lists for bots shots-
    bot_shots = []
    bot_targets = []

    turn = 1
    while player_ships and bot_ships:
        print(f"\n--- Turn {turn} ---")

        # -player boards print-
        print("Your board (your ships + bot hits):")
        print_board(player_board)

        # -bots board(w your hits-
        print("Bot board (your hits/misses):")
        print_board(bot_board)

        # -players move-
        try:
            x, y = map(int, input("Enter your shot (x y): ").split())
        except:
            print("Invalid input! Enter two numbers separated by space.")
            continue

        if not is_inside_board(x, y):
            print("Shot out of board! Enter numbers 0-9.")
            continue

        #checks if u hit bots ship
        hit, ship = check_hit((x, y), bot_ships)
        bot_board[x][y] = "X" if hit else "O"

        if hit and ship is not None and len(ship) == 0:
            destroyed_cells = [(x, y)]
            for sx, sy in destroyed_cells:
                for nx, ny in get_neighbors(sx, sy):
                    if bot_board[nx][ny] == ".":
                        bot_board[nx][ny] = "O"
            print("You destroyed a ship!")
        else:
            print("You hit!" if hit else "You miss!")

        # -bots move-
        if bot_targets:
            bx, by = bot_targets.pop(0)
        else:
            while True:
                bx, by = random.randint(0, 9), random.randint(0, 9)
                if (bx, by) not in bot_shots:
                    break
        bot_shots.append((bx, by))

        #check if bot hit your ship
        hit, ship = check_hit((bx, by), player_ships)
        player_board[bx][by] = "X" if hit else "O"

        if hit and ship is not None and len(ship) == 0:
            destroyed_cells = [(bx, by)]
            for sx, sy in destroyed_cells:
                for nx, ny in get_neighbors(sx, sy):
                    if player_board[nx][ny] == ".":
                        player_board[nx][ny] = "O"
            print(f"Bot destroyed your ship at {bx},{by}!")
            bot_targets = []
        else:
            print(f"Bot shoots: {bx},{by} -> {'hit' if hit else 'miss'}")

        turn += 1

    if not player_ships:
        print("Bot wins! sorry bro")
    else:
        print("You win, pozdravlyayu!")
