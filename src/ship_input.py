from src.utils import is_inside_board, is_valid_ship, create_empty_board, print_board
import csv

ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

board = create_empty_board()
occupied_cells = set()

#function to get ship cells from user input
def get_ship_cells(size):
    while True:
        coords = input(f"Enter ship of size {size} as x1,y1-x2,y2: ")
        try:
            start, end = coords.split('-')
            x1, y1 = map(int, start.split(','))
            x2, y2 = map(int, end.split(','))
        except:
            print("Wrong format, try again.")
            continue

         # определяем клетки корабля
        if x1 == x2:  # вертикальный корабль
            cells = [(x1, y) for y in range(min(y1, y2), max(y1, y2)+1)]
        elif y1 == y2:  # горизонтальный корабль
            cells = [(x, y1) for x in range(min(x1, x2), max(x1, x2)+1)]
        else:
            print("Ship must be straight!")
            continue

        # проверка размера и правил
        if len(cells) != size:
            print(f"Ship must have size {size}.")
            continue
        if not all(is_inside_board(x, y) for x, y in cells):
            print("Ship goes outside the board!")
            continue
        if not is_valid_ship(cells, occupied_cells):
            print("Ship touches another ship! Try again.")
            continue

        # добавляем корабль на поле
        for x, y in cells:
            board[y][x] = 'O'
            occupied_cells.add((x, y))
        print_board(board)
        return cells

# основная функция для всех кораблей
def get_player_ships():
    ships = []
    for size in ship_sizes:
        cells = get_ship_cells(size)
        ships.append(cells)

    # сохраняем в CSV
    with open("data/player_ships.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ship_id", "x", "y"])
        for i, ship in enumerate(ships, start=1):
            for x, y in ship:
                writer.writerow([i, x, y])
    print("All ships placed and saved!")

# вызываем функцию, чтобы игрок начал расставлять корабли
if __name__ == "__main__":
    get_player_ships()

