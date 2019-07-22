######################################################
## File Name: AIClass.py                            ##
## Description: AI Class for the Game               ##
######################################################

import math
from PlayerClasses import Player

INFINITY = math.inf

class AI(Player):
    depth = 0
    currentDepth = 0
    showScores = False

    def __init__(self, chip='X', difficulty=1, showScores='n'):
        super(AI, self).__init__(chip)
        self.setDifficulty(difficulty)
        self.logScores(showScores)

    def setDifficulty(self, difficulty):
        self.depth = difficulty

    def logScores(self, showScores):
        if showScores == 'y':
            self.showScores = True

    def playTurn(self, board):
        move = self.alphaBetaSearch(board)
        board.addChip(self.chip, move[0], move[1])
        return move

    def generateMoves(self, board):
        possibleMoves = []
        for column in range(board.boardWidth):
            move = board.canAddChip(column)
            if move[0]:
                possibleMoves.append((move[1], column))
        return possibleMoves

    def evaluateHeuristic(self, board):
        horizontalScore = 0
        verticalScore = 0
        firstDiagonalScore = 0
        secondDiagonalScore = 0

        for row in range(board.boardHeight - 3):
            for column in range(board.boardWidth):
                score = self.scorePosition(board, row, column, 1, 0)
                verticalScore += score

        for row in range(board.boardHeight):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, 0, 1)
                horizontalScore += score

        for row in range(board.boardHeight - 3):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, 1, 1)
                firstDiagonalScore += score

        for row in range(3, board.boardHeight):
            for column in range(board.boardWidth - 3):
                score = self.scorePosition(board, row, column, -1, 1)
                secondDiagonalScore += score

        return horizontalScore + verticalScore + firstDiagonalScore + secondDiagonalScore

    def scorePosition(self, board, row, column, deltaRow, deltaCol):
        humanScore = 0
        AIScore = 0
        humanPoints = 0
        AIPoints = 0

        for i in range(4):
            currentChip = board.getChip(row, column)

            if currentChip == self.chip:
                AIPoints += 1
            elif currentChip == 'O':
                humanPoints += 1

            row += deltaRow
            column += deltaCol

        if humanPoints == 1:
            humanScore = -1
        elif humanPoints == 2:
            humanScore = -10
        elif humanPoints == 3:
            humanScore = -100
        elif humanPoints == 4:
            humanScore = -1000

        if AIPoints == 1:
            AIScore = 1  # 1 point
        elif AIPoints == 2:
            AIScore = 10  # 10 points
        elif AIPoints == 3:
            AIScore = 100  # 100 points
        elif AIPoints == 4:
            AIScore = 1000  # 1000 points

        return humanScore + AIScore

    def alphaBetaSearch(self, state):
        self.currentDepth = 0
        scores = []
        bestAction = None
        v = max_value = -INFINITY
        alpha = -INFINITY
        beta = INFINITY
        actions = self.generateMoves(state)

        for action in actions:
            state.addChip(self.chip, action[0], action[1])
            v = self.minValue(state, alpha, beta)
            scores.append(v)
            if self.showScores:
                print("SCORE: ", v)
            if v > max_value:
                bestAction = action
                max_value = v
                alpha = max(alpha, max_value)
            self.currentDepth -= 1
            state.removeChip(action[0], action[1])

        if len(scores) == 1:
            bestAction = actions[0]

        return bestAction

    def maxValue(self, state, alpha, beta):
        self.currentDepth += 1
        actions = self.generateMoves(state)

        if not actions or self.currentDepth >= self.depth:
            score = self.evaluateHeuristic(state)
            return score
        else:
            v = -INFINITY
            for action in actions:
                state.addChip(self.chip, action[0], action[1])
                v = max(v, self.minValue(state, alpha, beta))

                if v >= beta:
                    self.currentDepth -= 1
                    state.removeChip(action[0], action[1])
                    return v

                alpha = max(v, alpha)
                self.currentDepth -= 1
                state.removeChip(action[0], action[1])

            return v

    def minValue(self, state, alpha, beta):
        self.currentDepth += 1
        actions = self.generateMoves(state)

        if not actions or self.currentDepth >= self.depth:
            score = self.evaluateHeuristic(state)
            return score
        else:
            v = INFINITY
            for action in actions:
                state.addChip('O', action[0], action[1])
                v = min(v, self.maxValue(state, alpha, beta))

                if v <= alpha:
                    self.currentDepth -= 1
                    state.removeChip(action[0], action[1])
                    return v

                beta = min(v, beta)
                self.currentDepth -= 1
                state.removeChip(action[0], action[1])

            return v