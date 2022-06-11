from flask import Flask
from flask_restful import Resource,Api,reqparse,abort
from service import validateMove, isGameWon, isBoardFilled, makeMove, togglePlayer
import numpy as np

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
        "board": "O--O---XX",
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
    global GAMES
    for game in GAMES:
        if game['game_id'] == game_id:
            return game
    abort(404, message="Game {} doesn't exist".format(game_id))


class GamesList(Resource):

    def get(self):
        return GAMES, 200

    #startGame
    def post(self):
        global game_number
        args = parser.parse_args()
        #TODO: change to random UUID
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
        modifiedGameData = list(args.board)
        print("ModifiedGameData", modifiedGameData)        

        global GAMES
        
        found_game = find_game(game_id)
        print("Found Game", found_game)
        oldGameData = list(found_game['board'])
        print("OldGameData", oldGameData)
        #TODO: set the player who is playing now
        player = 'O'
        # validate move
        if(not validateMove(modifiedGameData,oldGameData,player)):
            return "Bad Request", 400
        else:
            #TODO: check success
            twoDModifiedgameData = np.reshape(modifiedGameData, (3,3))
            gameWon = isGameWon(twoDModifiedgameData,player)
            print(gameWon)

            GAMES = [args if game['game_id'] == found_game['game_id'] else game for game in GAMES]

            #TODO: now make our own computer's move if the board is already not full, otherwise return status
            if(not isBoardFilled(twoDModifiedgameData)):
                #TODO: might need to remove toggling computer
                computer = togglePlayer(player)
                newGameData = makeMove(twoDModifiedgameData, computer)
                
                #check again, if the game is won after computer makes the move
                gameWon = isGameWon(newGameData,computer)
                print(gameWon)



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