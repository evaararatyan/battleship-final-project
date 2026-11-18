import csv
import random
from src.utils import (
    BOARD_SIZE,
    create_empty_board,
    print_board,
    is_inside_board,
    get_neighbors,
)

GAME_STATE_FILE = "data/game_state.csv"


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
            ship = [(int(row[i]), int(row[i + 1])) for i in range(0, len(row), 2)]
            ships.append(ship)
    return ships


def check_hit(shot, ships):
    """
    Check if a shot hits any ship.
    Removes the hit cell from the ship.
    Returns: (hit, ship_index, destroyed)
    """
    for i, ship in enumerate(ships):
        if shot in ship:
            ship.remove(shot)
            return True, i, len(ship) == 0
    return False, None, False


def mark_perimeter(board, ship_cells):
    """
    Mark all empty cells around a destroyed ship as misses.
    ship_cells = ORIGINAL cells of the ship (before they were removed).
    """
    for sx, sy in ship_cells:
        for nx, ny in get_neighbors(sx, sy):
            if board[nx][ny] == ".":
                board[nx][ny] = "O"


def is_available(board, cell):
    """Cell was not shot yet (not X and not O)."""
    x, y = cell
    return board[x][y] not in ("X", "O")


def bot_pick_targets(hits, board):
    """
    Candidate cells after the bot hit a ship but did not destroy it.
    1 hit   -> 4 orthogonal neighbours.
    2+ hits -> axis is locked: continue along the line at both ends.
    """
    if len(hits) == 1:
        x, y = hits[0]
        candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    else:
        xs = [h[0] for h in hits]
        ys = [h[1] for h in hits]
        if len(set(xs)) == 1:  # same row -> horizontal ship
            x = xs[0]
            candidates = [(x, min(ys) - 1), (x, max(ys) + 1)]
        else:  # same column -> vertical ship
            y = ys[0]
            candidates = [(min(xs) - 1, y), (max(xs) + 1, y)]
    return [c for c in candidates if is_inside_board(*c) and is_available(board, c)]


def log_move(turn, who, x, y, result):
    with open(GAME_STATE_FILE, "a", newline="") as f:
        csv.writer(f).writerow([turn, who, x, y, result])


def run_game():
    """
    Run the Battleship game loop.
    Shows both boards: player's and bot's (only hits/misses).
    """
    # -empty boards-
    player_board = create_empty_board()
    bot_board = create_empty_board()

    # -ships from csv (+ copies of original cells for perimeter marking)-
    player_ships = load_ships("data/player_ships.csv")
    bot_ships = load_ships("data/bot_ships.csv")
    player_original = [list(s) for s in player_ships]
    bot_original = [list(s) for s in bot_ships]

    # -place player ships on board-
    for ship in player_ships:
        for x, y in ship:
            player_board[x][y] = "S"

    # -bot state: hits on the current ship and queue of cells to check-
    bot_hits = []
    bot_targets = []

    # -log file with header-
    with open(GAME_STATE_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["turn", "who", "x", "y", "result"])

    turn = 1
    while any(player_ships) and any(bot_ships):
        print(f"\n--- Turn {turn} ---")

        print("Your board (your ships + bot hits):")
        print_board(player_board)
        print("Bot board (your hits/misses):")
        print_board(bot_board)

        # -player move-
        try:
            x, y = map(int, input("Enter your shot (x y): ").split())
        except ValueError:
            print("Invalid input! Enter two numbers separated by space.")
            continue

        if not is_inside_board(x, y):
            print("Shot out of board! Enter numbers 0-9.")
            continue

        if not is_available(bot_board, (x, y)):
            print("You already shot there! Choose another cell.")
            continue

        hit, idx, destroyed = check_hit((x, y), bot_ships)
        bot_board[x][y] = "X" if hit else "O"

        if destroyed:
            mark_perimeter(bot_board, bot_original[idx])
            print("You destroyed a ship!")
            log_move(turn, "player", x, y, "destroyed")
        else:
            print("You hit!" if hit else "You miss!")
            log_move(turn, "player", x, y, "hit" if hit else "miss")

        if not any(bot_ships):
            break

        # -bot move-
        bot_targets = [c for c in bot_targets if is_available(player_board, c)]
        if bot_targets:
            bx, by = bot_targets.pop(0)
        else:
            free = [
                (i, j)
                for i in range(BOARD_SIZE)
                for j in range(BOARD_SIZE)
                if is_available(player_board, (i, j))
            ]
            bx, by = random.choice(free)

        hit, idx, destroyed = check_hit((bx, by), player_ships)
        player_board[bx][by] = "X" if hit else "O"

        if destroyed:
            mark_perimeter(player_board, player_original[idx])
            bot_hits = []
            bot_targets = []
            print(f"Bot destroyed your ship at {bx},{by}!")
            log_move(turn, "bot", bx, by, "destroyed")
        elif hit:
            bot_hits.append((bx, by))
            bot_targets = bot_pick_targets(bot_hits, player_board)
            print(f"Bot shoots: {bx},{by} -> hit")
            log_move(turn, "bot", bx, by, "hit")
        else:
            print(f"Bot shoots: {bx},{by} -> miss")
            log_move(turn, "bot", bx, by, "miss")

        turn += 1

    if not any(player_ships):
        print("Bot wins!")
    else:
        print("You win, congratulations!")