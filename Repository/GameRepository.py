from Model.Game import Game

class GameRepository:
    def __init__(self):
        self.games = [
            {
                "game_id": "1",
                "board": "X--------",
                "status": "RUNNING"
            },
            {
                "game_id": "2",
                "board": "O--O---XX",
                "status": "RUNNING"
            },
            {
                "game_id": "3",
                "board": "X-----O--",
                "status": "RUNNING"
            }
        ]
    
    def get_games(self):
        return self.games

    def get_game(self, game_id):
        # logic
        for game in self.games:
            if game['game_id'] == game_id:
                return game
        #abort(404, message="Game {} doesn't exist".format(game_id))
        return None
        
    def add_game(self, game):
        self.games.append(game.toJSON())

    def delete_game(self, game_id):
        game = self.get_game(game_id)
        self.games.remove(game)
        return True

    #change datastructure to dictionary for easier update
    def update_game(self, game_id, game):
        self.games = [game.toJSON() if ele['game_id']== game_id else ele for ele in self.games]
        print(self.games)