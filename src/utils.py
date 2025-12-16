BOARD_SIZE = 10

def is_inside_board(x, y):
    """
    Check if coordinate is inside the board.
    """
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def get_neighbors(x, y):
    """
    Get all neighbor cells (including diagonals).
    """
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if is_inside_board(nx, ny):
                neighbors.append((nx, ny))
    return neighbors


def is_straight_line(ship):
    """
    Check that ship is in one row or one column.
    """
    xs = [x for x, _ in ship]
    ys = [y for _, y in ship]
    return len(set(xs)) == 1 or len(set(ys)) == 1

def is_consecutive(ship):
    """
    Check that ship cells are next to each other.
    """
    ship = sorted(ship)
    for i in range(len(ship) - 1):
        x1, y1 = ship[i]
        x2, y2 = ship[i + 1]
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return False
    return True


def is_valid_ship(ship_cells, occupied_cells):
    """
    Check that ship does not touch other ships.
    """
    for (x, y) in ship_cells:
        if (x, y) in occupied_cells:
            return False

        for neighbor in get_neighbors(x, y):
            if neighbor in occupied_cells:
                return False

    return True


def create_empty_board():
    """
    Create empty 10x10 board.
    """
    board = []
    for _ in range(BOARD_SIZE):
        board.append(["."] * BOARD_SIZE)
    return board


def print_board(board):
    """
    Print board to terminal.
    """
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(i, " ".join(row))
