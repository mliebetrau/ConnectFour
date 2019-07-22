######################################################
## File Name: GameBoard.py                          ##
## Description: Board Class for the Game            ##
######################################################

class GameBoard:
    board = []
    boardWidth = 7
    boardHeight = 6

    def __init__(self):
        self.setBoard()

    def setBoard(self):
        for row in range(self.boardHeight):
            self.board.append([])
            for column in range(self.boardWidth):
                self.board[row].append('-')

    def resetBoard(self):
        for row in range(self.boardHeight):
            for column in range(self.boardWidth):
                self.board[row][column] = '-'

    def printBoard(self):
        for i in range(self.boardHeight):
            print("| ", end="")
            print(*self.board[i], sep=" | ", end="")
            print(" |\n")

    def isValidColumn(self, column):
        return False if column < 0 or column >= self.boardWidth else True

    def getChip(self, row, column):
        return self.board[row][column]

    def canAddChip(self, column):
        for i in range((self.boardHeight - 1), -1, -1):
            if self.board[i][column] == '-':
                return True, i
        return False, -1

    def addChip(self, chip, row, column):
        self.board[row][column] = chip

    def removeChip(self, row, column):
        self.board[row][column] = '-'

    def isWinner(self, chip):
        ticks = 0

        #----- Vertical -----#
        for row in range(self.boardHeight - 3):
            for column in range(self.boardWidth):
                ticks = self.checkAdjacent(chip, row, column, 1, 0)
                if ticks == 4:
                    return True

        #----- Horizontal -----#
        for row in range(self.boardHeight):
            for column in range(self.boardWidth - 3):
                ticks = self.checkAdjacent(chip, row, column, 0, 1)
                if ticks == 4:
                    return True

        # ----- Positive slope diagonal -----#
        for row in range(self.boardHeight - 3):
            for column in range(self.boardWidth - 3):
                ticks = self.checkAdjacent(chip, row, column, 1, 1)
                if ticks == 4:
                    return True

        # ----- Negative slope diagonal -----#
        for row in range(3, self.boardHeight):
            for column in range(self.boardWidth - 5):
                ticks = self.checkAdjacent(chip, row, column, -1, 1)
                if ticks == 4:
                    return True

        return False

    def checkAdjacent(self, chip, row, column, deltaRow, deltaCol):
        count = 0
        for i in range(4):
            currentChip = self.getChip(row, column)
            if currentChip == chip:
                count += 1
            row += deltaRow
            column += deltaCol
        return count