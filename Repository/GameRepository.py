"""
This file is the repository/database
that holds the games dictionary
and database CRUD functions
"""

from Utils.utils import to_object


class GameRepository:
    def __init__(self):
        """dictionary which holds the state of all games"""
        self.games = {
            "1": {
                "game_id": "1",
                "board": "X--------",
                "status": "RUNNING",
                "player": "O",
                "computer": "X",
            },
            "2": {
                "game_id": "2",
                "board": "O--O---XX",
                "status": "RUNNING",
                "player": "O",
                "computer": "X",
            },
            "3": {
                "game_id": "3",
                "board": "X-----O--",
                "status": "RUNNING",
                "player": "X",
                "computer": "O",
            },
        }

    def get_games(self):
        return self.games

    def get_game(self, game_id):
        if game_id in self.games.keys():
            return self.games[game_id]
        return None

    def add_game(self, game):
        self.games[game.game_id] = game.to_json()

    def delete_game(self, game_id):
        if game_id in self.games.keys():
            del self.games[game_id]
            return True
        else:
            return False

    def update_game(self, game_id, game):
        if game_id in self.games.keys():
            self.games[game_id] = game.to_json()
            print(self.games)
            return True
        else:
            return False
