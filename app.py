"""
This is the main script to start the backend APIs
"""
from flask import Flask
from flask_restful import Resource, Api
from Utils.utils import to_object


from Service.GameService import GameService
from Utils.utils import get_args_parser

app = Flask(__name__)
api = Api(app)


game_service = GameService()

# get parser from utils.py
parser = get_args_parser()


class GamesList(Resource):
    """ """

    def get(self):
        """
        The Get Method API
        Fetch all Games
        """
        games = game_service.get_games()

        # collect all values of "games" dictionary and map each item to desired object structure
        gamesList = [to_object(v) for v in games.values()]
        return {"message": "Success", "data": gamesList}, 200

    def post(self):
        """The Post Method API
        Start a game

        Returns:
            Response: on success,the Game object in json format and status code

        """
        args = parser.parse_args()
        game = game_service.start_game(args["board"])
        if game is not None:
            return {"message": "Success", "data": to_object(game)}, 200
        else:
            return {"message": "Bad Request"}, 400


class Games(Resource):
    def get(self, game_id):
        """The Get API Method

        Args:
            game_id (string): the unique GameId

        Returns:
            Response: the game object and response code
        """

        game = game_service.get_game(game_id)
        if game:
            return {"message": "Success", "data": to_object(game)}, 200
        else:
            return {"message": "Resource not found"}, 404

    def put(self, game_id):
        """Update the Game

        Args:
            game_id (string): The GameId
        """
        args = parser.parse_args()
        game, message = game_service.update_game(game_id, args)
        if game is not None:
            return {
                "message": "Move successfully registered",
                "data": to_object(game),
            }, 200
        else:
            return {"message": f"Move not registered : {message}"}, 400

    def delete(self, game_id):
        """Delete the Game

        Args:
            game_id (string): Game Id

        Returns:
            Response: response object and status code
        """
        game = game_service.get_game(game_id)
        if not game:
            return {"message": "Resource not found"}, 404
        else:
            if game_service.delete_game(game_id):
                return {"message": "Game successfully deleted"}, 200
            else:
                return {"message": "Bad Request"}, 400


api.add_resource(GamesList, "/games")
api.add_resource(Games, "/games/<game_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
