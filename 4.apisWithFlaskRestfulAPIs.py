from flask import Flask
from flask_restful import Resource,Api,reqparse,abort
app = Flask(__name__)
api = Api(app)


#TODO: define skeleton class/model for GAMES
GAMES = [
    {
        "game_id": "1",
        "board": "X--------",
        "status": "RUNNING"
    },
    {
        "game_id": "2",
        "board": "X--X--O---",
        "status": "RUNNING"
    },
    {
        "game_id": "3",
        "board": "X-----O--",
        "status": "RUNNING"
    }
]

#TODO: Change this assignment to zero when GAMES is not initialized
game_number = len(GAMES)

parser = reqparse.RequestParser()  # initialize
parser.add_argument('game_id')  # add args
parser.add_argument('board', required=True)
parser.add_argument('status')

def find_game(game_id):
    for game in GAMES:
        if game['game_id'] == game_id:
            return game
        else:
            abort(404, message="Game {} doesn't exist".format(game_id))


class GamesList(Resource):

    def get(self):
        return GAMES, 200

    #startGame
    def post(self):
        global game_number
        args = parser.parse_args()
        game_number+=1
        args.game_id = game_number
        args.status = "RUNNING"
        print(args)
        GAMES.append(args)
        print(GAMES)
        return args, 200



    

class Games(Resource):
    #get Game
    def get(self,game_id):
        game = find_game(game_id)
        return game, 200

    #newMove
    #TODO: this is the API with most logic, integrate the logics here
    def put(self, game_id):
        args = parser.parse_args()

        global GAMES
        
        found_game = find_game(game_id)
        #TODO: validate move

        #TODO: check success

        GAMES = [args if game == found_game else game for game in GAMES]

        #TODO: now make our own computer's move if the board is already not full, otherwise return status

        returned_game = find_game(game_id) #change this after reflecting computers move
        return returned_game, 200

    # delete Game
    def delete(self, game_id):
        game = find_game(game_id)
        GAMES.remove(game)
        print(GAMES)
        return '', 200

api.add_resource(GamesList, '/games')
api.add_resource(Games, '/games/<game_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)