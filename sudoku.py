class Point(object):
    def __init__(self, point):
        self._point = point
        self._value = 0
        self._possibilities = []

    def setPossibileValues(self, possibilities):
        self._possibilities = possibilities

    def getPossibileValues(self):
        return self._possibilities

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
        self._possibilities = []

    def getCoords(self):
        return self._point

    def getPossibilityCount(self):
        return len(self._possibilities)

    def setOnlyPossibility(self):
        self.setValue(self._possibilities[0])

    def existsPossibility(self, possibility):
        return possibility in self._possibilities

    def __eq__(self, value):
        if self._value == value:
            return True
        return False

    def __repr__(self):
        return "Point: " + str(self._point) + " -> " + str(self._possibilities)

class Board(object):
    def __init__(self, filename):
        self._board = {}

        for point in sodoku_points():
            self._board[point] = Point(point)

        self._load(filename)

    def getPoint(self, point):
        return self._board[point]

    def _load(self, filename):
        points = sodoku_points()
        board_file = open(filename, 'r')
        for data_point in board_file.read():
            if data_point is not '\n':
                position = next(points)
                if data_point is not 'X':
                    self.getPoint(position).setValue(int(data_point))

    def show(self):
        for y in range(9):
            if y % 3 == 0:
                print("-" * 25)
            for x in range(9):
                if x % 3 == 0:
                    self._boardPrint('|')
                if self.getPoint((x, y)) == 0:
                    self._boardPrint(" ")
                else:
                    self._boardPrint(self.getPoint((x, y)).getValue())
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

    def __iter__(self):
        return iter(self._board.items())

    def __getitem__(self, point):
        return self._board[point]

class Solver(object):
    def __init__(self, board):
        self._board = board
        self._possibilities = []

    def findPossibilities(self):
        for point in sodoku_points():
            if self._board.getPoint(point) == 0:

                self._possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                for position in self._board.getSquare(point):
                    self._checkPossibility(position)

                for position in self._board.getRow(point):
                    self._checkPossibility(position)

                for position in self._board.getColumn(point):
                    self._checkPossibility(position)

                self._board.getPoint(point).setPossibileValues(self._possibilities)


    def _checkPossibility(self, position):
        check_value = self._board.getPoint(position).getValue()
        if check_value in self._possibilities:
            self._possibilities.remove(check_value)

    def _isSquareUnique(self, coords, possibility):
        for check_position in self._board.getSquare(coords):
            if possibility in self._board.getPoint(check_position).getPossibileValues() and check_position != coords:
                return False

        return True

    def _isRowUnique(self, coords, possibility):
        for check_position in self._board.getRow(coords):
            if possibility in self._board.getPoint(check_position).getPossibileValues() and check_position != coords:
                return False

        return True

    def _isColumnUnique(self, coords, possibility):
        for check_position in self._board.getColumn(coords):
            if possibility in self._board.getPoint(check_position).getPossibileValues() and check_position != coords:
                return False

        return True

    def _isLineUnique(self, coords, possibility):
        if self._isRowUnique(coords, possibility) or self._isColumnUnique(coords, possibility):
            return True
        return False

    def _isUnique(self, coords, possibility):
        if self._isLineUnique(coords, possibility) or self._isSquareUnique(coords, possibility):
            return True
        return False

    def applyPossibilities(self):
        for coords, point in self._board:
            if point.getPossibilityCount() == 1:
                point.setOnlyPossibility()

            # Find the new possibilities for uniquness to run.
            self.findPossibilities()

            for point_possibility in point.getPossibileValues():
                if self._isUnique(coords, point_possibility):
                    point.setValue(point_possibility)

    def isSolved(self):
        for point in sodoku_points():
            if self._board.getPoint(point) == 0:
                return False
        return True

def sodoku_points():
    """ A method used to generate the points required for loading and checking
    the sodoku grid.

    sodoku_points -> Generator((int, int))

    """
    for y in range(9):
        for x in range(9):
            yield (x, y)

le_board = Board("board3.txt")
le_board.show()

le_solver = Solver(le_board)

while(not le_solver.isSolved()):
    le_solver.findPossibilities()

    inp = ""
    inp = input("")
    if inp == "p":
        for point in sodoku_points():
                if le_board.getPoint(point).getPossibilityCount() != 0:
                    print(str(point) + " -> " + str(le_board.getPoint(point).getPossibileValues()))


    le_solver.applyPossibilities()


    if inp == "s" or inp == "p":
        le_board.show()

le_board.show()
