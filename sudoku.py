class Board(object):
    def __init__(self, filename):
        self._board = {}

        for point in sodoku_points():
            self._board[point] = {}
            self._board[point]['current'] = 0
            self._board[point]['possible'] = []

        self._load(filename)

    def getCurrent(self, point):
        return self._board[point]['current']

    def setCurrent(self, point, value):
        self._board[point]['current'] = value

    def setPossibilities(self, point, possibilities):
        self._board[point]['possible'] = possibilities

    def getPossibilities(self, point):
        return self._board[point]['possible']

    def getNumberOfPossibilities(self, point):
        return len(self._board[point]['possible'])

    def _load(self, filename):
        position_iterator = Position_Iterator()
        board_file = open(filename, 'r')
        for data_point in board_file.read():
            if data_point is not '\n':
                position = next(position_iterator)
                if data_point is not 'X':
                    self._board[position]['current'] = int(data_point)

    def show(self):
        for y in range(9):
            if y % 3 == 0:
                print("-" * 25)
            for x in range(9):
                if x % 3 == 0:
                    self._boardPrint('|')
                if self._board[x, y]['current'] == 0:
                    self._boardPrint(" ")
                else:
                    self._boardPrint(self._board[x, y]['current'])
            print("|")
        print("-" * 25)

    @staticmethod
    def _boardPrint(le_string):
        print(le_string, end=' ')

    @staticmethod
    def getSquare(point):
        square_points = []
        x_i, y_i = point
        x = (x_i // 3) * 3
        y = (y_i // 3) * 3
        for i in range(3):
            for j in range(3):
                square_points.append((x + i, y + j))

        return square_points

    @staticmethod
    def getRow(point):
        row_points = []
        x_i, y_i = point
        for i in range(9):
            row_points.append((i, y_i))
        return row_points

    @staticmethod
    def getColumn(point):
        column_points = []
        x_i, y_i = point
        for i in range(9):
            column_points.append((x_i, i))
        return column_points


class Solver(object):
    def __init__(self, board):
        self._board = board

    def findPossibilities(self):
        for point in sodoku_points():
            if self._board.getCurrent(point) == 0:

                possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for position in self._board.getSquare(point):
                    if self._board.getCurrent(position) in possibilities:
                        possibilities.remove(self._board.getCurrent(position))

                for position in self._board.getRow(point):
                    if self._board.getCurrent(position) in possibilities:
                        possibilities.remove(self._board.getCurrent(position))

                for position in self._board.getColumn(point):
                    if self._board.getCurrent(position) in possibilities:
                        possibilities.remove(self._board.getCurrent(position))

                self._board.setPossibilities(point, possibilities)

    def isSquareUnique(self, point, possibility):
        for position in self._board.getSquare(point):
            if possibility in self._board.getPossibilities(position) and position != point:
                return False

        return True

    def isRowUnique(self, point, possibility):
        for position in self._board.getRow(point):
            if possibility in self._board.getPossibilities(position) and position != point:
                return False

        return True

    def isColumnUnique(self, point, possibility):
        for position in self._board.getColumn(point):
            if possibility in self._board.getPossibilities(position) and position != point:
                return False

        return True

    def isLineUnique(self, point, possibility):
        if self.isRowUnique(point, possibility) or self.isColumnUnique(point, possibility):
            return True
        return False

    def isUnique(self, point, possibility):
        if self.isLineUnique(point, possibility) or self.isSquareUnique(point, possibility):
            return True
        return False

    def applyPossibilities(self):
        for point in sodoku_points():
            if self._board.getNumberOfPossibilities(point) == 1:
                self._board.setCurrent(point,
                    self._board.getPossibilities(point)[0])
            for possibility in self._board.getPossibilities(point):
                if self.isUnique(point, possibility):
                    self._board.setCurrent(point, possibility)

        for point in sodoku_points():
            if self._board.getCurrent(point) > 0 and self._board.getNumberOfPossibilities(point) != 0:
                self._board.setPossibilities(point, [])

    def isSolved(self):
        for point in sodoku_points():
            if self._board.getCurrent(point) == 0:
                return False
        return True

def Position_Iterator():
    x = 0
    y = 0

    while y < 9:
        yield (x, y)

        x += 1

        if x == 9:
            x = 0
            y += 1

def sodoku_points():
    for x in range(9):
        for y in range(9):
            yield (x, y)

le_board = Board("board3.txt")
le_board.show()

le_solver = Solver(le_board)

iterations = 0

while(not le_solver.isSolved()):
    iterations += 1
    le_solver.findPossibilities()
    le_solver.applyPossibilities()

    le_board.show()
    inp = input("")
    if inp == "p":
        for point in sodoku_points():
                if le_board.getPossibilities(point) != []:
                    print(str(point) + " -> " + str(le_board.getPossibilities(point)))

le_board.show()
print(iterations)
