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
                ship.remove(shot)  # убираем попадание из корабля
                return True, ship
        return False, None

    # --- Создание пустых досок ---
    player_board = create_empty_board()  # доска игрока
    bot_board = create_empty_board()     # доска бота (для отображения твоих попаданий)

    # --- Загрузка кораблей из CSV ---
    player_ships = load_ships("data/player_ships.csv")
    bot_ships = load_ships("data/bot_ships.csv")

    # --- Списки для выстрелов бота ---
    bot_shots = []     # все клетки, по которым бот уже стрелял
    bot_targets = []   # список клеток для умного поиска после попадания

    turn = 1
    while player_ships and bot_ships:
        print(f"\n--- Turn {turn} ---")

        # --- Печать доски игрока ---
        print("Your board (your ships + bot hits):")
        print_board(player_board)

        # --- Печать доски бота (только твои выстрелы) ---
        print("Bot board (your hits/misses):")
        print_board(bot_board)

        # --- Ход игрока ---
        try:
            x, y = map(int, input("Enter your shot (x y): ").split())
        except:
            print("Invalid input! Enter two numbers separated by space.")
            continue

        if not is_inside_board(x, y):
            print("Shot out of board! Enter numbers 0-9.")
            continue

        # Проверка попадания по кораблям бота
        hit, ship = check_hit((x, y), bot_ships)
        bot_board[x][y] = "X" if hit else "O"
        
    
        if hit and ship is not None and len(ship) == 0:
        #   Корабль полностью уничтожен
            destroyed_cells = [(x, y)]  # здесь лучше передавать весь корабль
            for sx, sy in destroyed_cells:
                for nx, ny in get_neighbors(sx, sy):
                    if bot_board[nx][ny] == ".":
                        bot_board[nx][ny] = "O"
            print("You destroyed a ship!")  # <-- сообщение вместо обычного hit
        else:
            print("You hit!" if hit else "You miss!")



        # --- Ход бота ---
        # Если бот ранее попал и ищет соседние клетки (умный режим)
        if bot_targets:
            bx, by = bot_targets.pop(0)
        else:
        # Иначе случайный выстрел
            while True:
                bx, by = random.randint(0, 9), random.randint(0, 9)
                if (bx, by) not in bot_shots:
                    break
        bot_shots.append((bx, by))

    # Проверяем попадание по кораблям игрока
        hit, ship = check_hit((bx, by), player_ships)
        player_board[bx][by] = "X" if hit else "O"

    # Проверяем, полностью ли уничтожен корабль
        if hit and ship is not None and len(ship) == 0:
        # destroyed_cells — все клетки только что уничтоженного корабля
        # Здесь желательно, чтобы check_hit возвращал весь корабль до удаления клетки
            destroyed_cells = [(bx, by)]  # временно, можно улучшить позже

            # Отмечаем все соседние клетки как промах
            for sx, sy in destroyed_cells:
                for nx, ny in get_neighbors(sx, sy):
                    if player_board[nx][ny] == ".":
                        player_board[nx][ny] = "O"

            # Сообщение игроку о том, что корабль уничтожен
            print(f"Bot destroyed your ship at {bx},{by}!")

            # Сбрасываем цели бота после уничтожения корабля
            bot_targets = []
        else:
            print(f"Bot shoots: {bx},{by} -> {'hit' if hit else 'miss'}")

        turn += 1

    # End of the game
    if not player_ships:
        print("Bot wins! sorry bro")
    else:
        print("You win, pozdravlyayu!")
