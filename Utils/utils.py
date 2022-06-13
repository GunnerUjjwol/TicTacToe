"""
Utility functions and variables
"""
from flask_restful import reqparse
from enum import Enum


class GridValue(Enum):
    """
    Grid Value types Enum
    """
    Unfilled = "-"
    Cross = "X"
    Naught = "O"

class GameState(Enum):
    """
    Game State Enum 
    """
    RUNNING = "RUNNING"
    X_WON = "X_WON"
    O_WON = "O_WON"
    DRAW = "DRAW"


"""
The List of sets that contains the indices
which would signify the winning condition
if all specified indices in the list has same GridValue
"""
winningSets = [
    # row Match Indices
    {0, 1, 2},
    {3, 4, 5},
    {6, 7, 8},
    # column Match Indices
    {0, 3, 6},
    {1, 4, 7},
    {2, 5, 8},
    # diagonal Match indices
    {0, 4, 8},
    {2, 4, 6},
]

# utility function to toggle player


def toggle_player(player):
    """
    change player from naught to cross and viceversa

    Args:
        player (char): the player denotion

    Returns:
        _type_: _description_
    """
    player = GridValue.Cross.value if player == GridValue.Naught.value else GridValue.Naught.value
    return player


def get_args_parser():
    """
    add arguments to the requestparser
    to parse request body
    returns the requestparser
    """
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument("game_id")  # add args
    parser.add_argument("board", required=True)
    parser.add_argument("status")
    return parser


def to_object(gameJSON):
    """
    retains only the desirable keys and returns it as a new Object

    Args:
        gameJSON (json): the Json Object

    Returns:
        dict: the desired format dict
    """
    game_dict = {}
    game_dict["game_id"] = gameJSON.get("game_id")
    game_dict["board"] = gameJSON.get("board")
    game_dict["status"] = gameJSON.get("status")

    return game_dict
