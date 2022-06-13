"""
Model for Game Object
"""

from uuid import uuid1


class Game:
    def __init__(self):
        """
        Intialize the game
        """
        self.board = "---------"
        self.status = "RUNNING"
        self.game_id = str(uuid1())  # Gets a unique identifier
        self.player = "X"
        self.computer = "O"

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_game_id(self):
        return self.game_id

    def set_game_id(self, game_id):
        self.game_id = game_id

    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player

    def get_computer(self):
        return self.computer

    def set_computer(self, computer):
        self.computer = computer

    def to_json(self):
        """
        Utility function to convert Game Object to Json

        Returns:
            json: the json representation of game
        """
        return {
            "game_id": self.game_id,
            "status": self.status,
            "board": self.board,
            "player": self.player,
            "computer": self.computer,
        }
