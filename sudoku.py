sudoku_board = {}
SUDOKU_BOARD_SIZE = 9;

def Position_Iterator():
    x = 0
    y = 0

    while y < 9:
        yield (x, y)

        x += 1

        if x == 9:
            x = 0
            y += 1


def Print_Board(sudoku_board):
    for y in range(SUDOKU_BOARD_SIZE):
        if y % 3 == 0:
            print("-" * 25)
        for x in range(SUDOKU_BOARD_SIZE):
            if x % 3 == 0:
                prnt('|')
            if sudoku_board[x, y]['current'] == 0:
                prnt(" ")
            else:
                prnt(sudoku_board[x, y]['current'])
        print("|")
    print("-" * 25)


def Load_Board(filename):
    position_iterator = Position_Iterator()
    board_file = open(filename, 'r')
    for data_point in board_file.read():
        if data_point is not '\n':
            position = next(position_iterator)
            if data_point is not 'X':
                sudoku_board[position]['current'] = int(data_point)

def Get_Square(point):
    square_points = []
    x_i, y_i = point
    x = (x_i // 3) * 3
    y = (y_i // 3) * 3
    for i in range(3):
        for j in range(3):
            square_points.append((x + i, y + j))

    return square_points

def Get_Row(point):
    row_points = []
    x_i, y_i = point
    for i in range(9):
        row_points.append((i, y_i))
    return row_points

def Get_Column(point):
    column_points = []
    x_i, y_i = point
    for i in range(9):
        column_points.append((x_i, i))
    return column_points

def Find_Possibilities(sudoku_board):
    for x in range(SUDOKU_BOARD_SIZE):
        for y in range(SUDOKU_BOARD_SIZE):
            if sudoku_board[x, y]['current'] == 0:

                possibilities = [1,2,3,4,5,6,7,8,9]

                for position in Get_Square((x, y)):
                    if sudoku_board[position]['current'] in possibilities:
                        possibilities.remove(sudoku_board[position]['current'])

                for position in Get_Row((x, y)):
                    if sudoku_board[position]['current'] in possibilities:
                        possibilities.remove(sudoku_board[position]['current'])

                for position in Get_Column((x, y)):
                    if sudoku_board[position]['current'] in possibilities:
                        possibilities.remove(sudoku_board[position]['current'])



                sudoku_board[x, y]['possible'] = possibilities

def Is_Square_Unique(sudoku_board, point, possibility):
    for position in Get_Square(point):
        if possibility in sudoku_board[position]['possible'] and position != point:
            return False

    return True

def Is_Row_Unique(sudoku_board, point, possibility):
    for position in Get_Row(point):
        if possibility in sudoku_board[position]['possible'] and position != point:
            return False

    return True

def Is_Column_Unique(sudoku_board, point, possibility):
    for position in Get_Column(point):
        if possibility in sudoku_board[position]['possible'] and position != point:
            return False

    return True

def Is_Line_Unique(sudoku_board, point, possibility):
    if Is_Row_Unique(sudoku_board, point, possibility) or Is_Column_Unique(sudoku_board, point, possibility):
        return True
    return False


def Is_Unique(sudoku_board, point, possibility):
    if Is_Line_Unique(sudoku_board, point, possibility) or Is_Square_Unique(sudoku_board, point, possibility):
        return True
    return False

def Use_Possibilities(sudoku_board):
    for x in range(9):
        for y in range(9):
            if len(sudoku_board[x, y]['possible']) == 1:
                sudoku_board[x, y]['current'] = sudoku_board[x, y]['possible'][0]
            for possibility in sudoku_board[x, y]['possible']:
                if Is_Unique(sudoku_board, (x, y), possibility):
                    sudoku_board[x, y]['current'] = possibility

def Is_Solved(sudoku_board):
    for x in range(9):
        for y in range(9):
            if sudoku_board[x, y]['current'] == 0:
                return False

    return True

def prnt(le_string):
    print(le_string, end=' ')

for x in range(SUDOKU_BOARD_SIZE):
    for y in range(SUDOKU_BOARD_SIZE):
        sudoku_board[x, y] = {}
        sudoku_board[x, y]['current'] = 0
        sudoku_board[x, y]['possible'] = []

Load_Board("board4.txt")
Print_Board(sudoku_board)

iterations = 0

while(not Is_Solved(sudoku_board)):
    iterations += 1
    Find_Possibilities(sudoku_board)
    Use_Possibilities(sudoku_board)

    for x in range(9):
        for y in range(9):
            if sudoku_board[x, y]['current'] > 0 and len(sudoku_board[x, y]['possible']) != 0:
                sudoku_board[x, y]['possible'] = []

    Print_Board(sudoku_board)
    inp = input("")
    if inp == "p":
        for x in range(SUDOKU_BOARD_SIZE):
            for y in range(SUDOKU_BOARD_SIZE):
                if sudoku_board[x, y]['possible'] != []:
                    print(str(x)+ ", " + str(y) + " -> " + str(sudoku_board[x, y]['possible']))

Print_Board(sudoku_board)
print(iterations)
