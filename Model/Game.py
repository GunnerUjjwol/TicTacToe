from enum import Enum
from uuid import uuid1

#class for enum to identify unfilled value, cross and naught values
class GridValue(Enum):
    Unfilled = '-'
    Cross = 'X'
    Naught = 'O'

class State(Enum):
    RUNNING = "RUNNING"
    X_WON = "X_WON"
    O_WON = "O_WON"
    DRAW = "DRAW"

class Game:
    def __init__(self):
        self.board = "---------"
        self.status = State.RUNNING.value
        self.game_id = uuid1() #
    
    def get_board(self):
        return self.board

    def set_board(self, board):
        # have validation here

        self.board = board
    
    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_game_id(self):
        return self.game_id
    
