from flask_restful import reqparse


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
def togglePlayer(player):
    player = "O" if player == "X" else "X"
    return player


def getArgsParser():
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument("game_id")  # add args
    parser.add_argument("board", required=True)
    parser.add_argument("status")
    return parser
