import json
from flask import Flask
from flask_restful import Resource,Api,abort

from Utils import *
from Service.GameService import GameService
from Utils.utils import getArgsParser
app = Flask(__name__)
api = Api(app)


gameService = GameService()

#get parser from utils.py
parser = getArgsParser()


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