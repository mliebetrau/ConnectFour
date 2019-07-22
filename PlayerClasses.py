######################################################
## File Name: PlayerClasses.py                      ##
## Description: Player Classes for the Game         ##
######################################################

import sys
from abc import ABCMeta, abstractmethod

#------------------------------------------#
# Abstract Class for humans and AI players #
#------------------------------------------#

class Player(metaclass=ABCMeta):
    chip = ""

    def __init__(self, chip):
        self.chip = chip

    @abstractmethod
    def playTurn(self):
        pass

class Human(Player):

    def __init__(self, chip):
        super(Human, self).__init__(chip)

    def playTurn(self, board):
        column = int(input("Pick a column (enter -1 to quit playing) => "))

        if column == -1:
            sys.exit()

        column -= 1
        while True:
            if board.isValidColumn(column):
                row = board.canAddChip(column)
                if row[0]:
                    board.addChip(self.chip, row[1], column)
                    break
            column = int(input("That column did not work. Try a different column => "))
            column -= 1

        return row[1], column

