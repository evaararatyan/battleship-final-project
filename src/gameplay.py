import csv
import random
from src.utils import create_empty_board, print_board, is_inside_board

# --- Чтение CSV кораблей ---
def load_ships(filename):
    ships = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            # каждая строка: x1,y1,x2,y2,...
            ship = [(int(row[i]), int(row[i+1])) for i in range(0, len(row), 2)]
            ships.append(ship)
    return ships

# --- Проверка попадания ---
def check_hit(shot, ships):
    for ship in ships:
        if shot in ship:
            ship.remove(shot)
            return True
    return False

# --- Создание пустых досок ---
player_board = create_empty_board()
bot_board = create_empty_board()

player_ships = load_ships("data/player_ships.csv")
bot_ships = load_ships("data/bot_ships.csv")

# --- Список для ходов бота ---
bot_shots = []

# --- Игровой цикл ---
turn = 1
while player_ships and bot_ships:
    print(f"\n--- Turn {turn} ---")
    print("Your board:")
    print_board(player_board)

    # --- Ход игрока ---
    try:
        x, y = map(int, input("Enter your shot (x y): ").split())
    except:
        print("Invalid input")
        continue

    if not is_inside_board(x, y):
        print("Shot out of board!")
        continue

    hit = check_hit((x, y), bot_ships)
    player_board[x][y] = "X" if hit else "O"
    print("You hit!" if hit else "You miss!")

    # --- Ход бота ---
    while True:
        bx, by = random.randint(0, 9), random.randint(0, 9)
        if (bx, by) not in bot_shots:
            bot_shots.append((bx, by))
            break

    hit = check_hit((bx, by), player_ships)
    bot_board[bx][by] = "X" if hit else "O"
    print(f"Bot shoots: {bx},{by} -> {'hit' if hit else 'miss'}")

    turn += 1

# --- Конец игры ---
if not player_ships:
    print("Bot wins!")
else:
    print("You win!")
