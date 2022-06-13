"""
This file contains the actual logics 
and functions to fulfill the use cases
"""

import random

from Model.Game import Game
from Repository.GameRepository import GameRepository
from Utils.utils import winningSets, toggle_player, GridValue


class GameService:

    def __init__(self):
        self.game_repository = GameRepository()
        self.nRows = 3
        self.nCols = 3

    def get_games(self):
        return self.game_repository.get_games()

    def get_game(self, game_id):
        return self.game_repository.get_game(game_id)

    def delete_game(self, game_id):
        return self.game_repository.delete_game(game_id)

    def update_game(self, game_id, modifiedGame):
        game = Game()
        unModifiedGame = self.game_repository.get_game(game_id)

        if unModifiedGame is None:
            return False
        print("Found Game", unModifiedGame)
        oldGameBoard = unModifiedGame["board"]
        modifiedGameBoard = modifiedGame.board

        print("OldGameData", oldGameBoard)
        # obtain the symbol the player is playing with, Naught or Cross
        player = unModifiedGame["player"]
        # validate move
        print(modifiedGameBoard)
        if not self.validate_move(modifiedGame, unModifiedGame, player):
            return None
        else:

            gameWon = self.is_game_won(modifiedGameBoard, player)
            print("Game Won", gameWon)

            # now make our own computer's move if the board is already not full, otherwise return status
            if not self.is_board_filled(modifiedGameBoard):
                # TODO: might need to remove toggling computer
                player = toggle_player(player)
                modifiedGameBoard = self.make_move(modifiedGameBoard, player)

                # check again, if the game is won after computer makes the move
                gameWon = self.is_game_won(modifiedGameBoard, player)
                print("Game Won", gameWon)
                print(modifiedGameBoard)

            game.set_game_id(game_id)
            game.set_board(modifiedGameBoard)
            if gameWon:
                game.set_status(f"{player}_WON")
            else:
                if self.is_board_filled(modifiedGameBoard):
                    game.set_status("DRAW")
            self.game_repository.update_game(game_id, game)

            returned_game = self.game_repository.get_game(game_id)
            return returned_game.to_json()

    # initialize game Data after first post request to start a game
    # This is called upon post request to start the game
    def start_game(self, board):
        game = Game()

        boardData = list(board)
        # validate board
        if len(boardData) != 9:
            print("Invalid Board Data")
            return False
        game.set_board(board)
        tup = [(i, s) for i, s in enumerate(boardData) if s != "-"]
        print(tup)
        if len(tup) == 1:
            player = tup[0][1]
            computer = toggle_player(player)
            game.set_player(player)
            game.set_computer(computer)
            print(
                f"game initialized with player as: {player} and computer as: {computer}"
            )
            # make computer's move
            newBoard = self.make_move(boardData, computer)
            game.set_board(newBoard)
            self.game_repository.add_game(game)

            return game.to_json()

        elif len(tup) == 0:
            print("Game started with no initial move: ---------")
            print("Computer will make the first move")

            player = random.choice(
                [GridValue.Cross.value, GridValue.Naught.value])
            computer = toggle_player(player)
            game.set_player(player)
            game.set_computer(computer)
            print(game.__dict__)
            newGameData = self.make_move(boardData, computer)
            print(
                f"game initialized with player as: {player} and computer as: {computer}"
            )
            game.set_board(newGameData)
            self.game_repository.add_game(game)
            return game.to_json()

        else:
            print("Invalid Game Initialization")
            return None

    # define validation function
    def validate_move(self, newGameData, oldGameData, player):
        print(newGameData)
        print(oldGameData)
        newBoard = newGameData["board"]
        oldBoard = oldGameData["board"]
        if oldGameData["status"] != "RUNNING":
            print("Game Already Complete")
            return False
        if len(list(newBoard)) != 9:
            print("Invalid Board Data")
            return False
        newState = {(i, s) for i, s in enumerate(newBoard) if s in "XO"}
        oldState = {(i, s) for i, s in enumerate(oldBoard) if s in "XO"}
        print("oldState", oldState)
        print("newState", newState)
        if oldState <= newState:
            newMove = newState - oldState
            print("newMove", newMove)
            return len(newMove) == 1 and list(newMove)[0][1] == player
        else:
            return False

    def make_move(self, board, player):

        if not self.is_board_filled(board):
            board = list(board)
            print("One D Game Data", board)
            unfilledIndices = [
                idx for idx, ele in enumerate(board) if ele == GridValue.Unfilled.value
            ]
            print("Unfilled:", unfilledIndices)
            randomInt = random.choice(unfilledIndices)
            print("Grid position for new move", randomInt)
            board[randomInt] = player
            board = "".join(map(str, board))
            print("New Game Data\n", board)
            return board
        else:
            return board

    def is_board_filled(self, board):
        print("GridValue", GridValue.Unfilled.value)

        board = list(board)
        print(board)
        print(set(board))
        isFull = GridValue.Unfilled.value not in set(board)

        print("isFull", isFull)
        return isFull

    def is_game_won(self, board, player):
        # initialize to winningSets loaded from utils.py
        winSets = winningSets
        print("Board", board)
        playersGrid = {idx for idx, ele in enumerate(board) if ele == player}

        print(playersGrid)
        return any(winSet <= playersGrid for winSet in winSets)
