BOARD_SIZE = 10

# check: is cell inside the board or not
def is_inside_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

# get all neighboring cells of a given cell (even diagonals)
def get_neighbors(x, y):
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


# check if ship can be placed at given cells
def is_valid_ship(ship_cells, occupied_cells):
    for (x, y) in ship_cells:
        # if cell is already occupied
        if (x, y) in occupied_cells:
            return False

        # check neighboring cells
        for neighbor in get_neighbors(x, y):
            if neighbor in occupied_cells:
                return False
    return True


#creating empty board 10x10
def create_empty_board():
    board = []
    for _ in range(BOARD_SIZE):
        board.append(["."] * BOARD_SIZE)
    return board


#print the board in terminal
def print_board(board):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(i, " ".join(row))



