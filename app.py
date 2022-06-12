import json
from flask import Flask
from flask_restful import Resource,Api,reqparse,abort
from Service.GameService import GameService
app = Flask(__name__)
api = Api(app)


gameService = GameService()

parser = reqparse.RequestParser()  # initialize
parser.add_argument('game_id')  # add args
parser.add_argument('board', required=True)
parser.add_argument('status')

def find_game(game_id):
    global GAMES
    for game in GAMES:
        if game['game_id'] == game_id:
            return game
    abort(404, message="Game {} doesn't exist".format(game_id))


class GamesList(Resource):

    def get(self):
        return gameService.get_games(), 200

    #startGame
    def post(self):
        args = parser.parse_args() 
        game = gameService.startGame(args['board'])
        if game:
            return game.toJSON(), 200
        else:
             return 'Bad Request', 400
  

class Games(Resource):
    #get Game
    def get(self,game_id):
        game = gameService.get_game(game_id)
        if game:
            return game, 200
        else:
            return "Resource not found", 404

    #newMove
    #TODO: this is the API with most logic, integrate the logics here
    def put(self, game_id):
        args = parser.parse_args()
        gameService.update_game(game_id,args)  
        return 
    # delete Game
    def delete(self, game_id):
        game = gameService.get_game(game_id)
        if not game:
            return "Resource not Found", 404
        else:
            if gameService.delete_game(game_id):
                return "Game Successfully deleted", 200
            else:
                return "Internal Server Error", 200

api.add_resource(GamesList, '/games')
api.add_resource(Games, '/games/<game_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)