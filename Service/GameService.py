"""
This file contains the actual logics 
and functions to fulfill the use cases
"""

import random

from Model.Game import Game
from Repository.GameRepository import GameRepository
from Utils.utils import winningSets, toggle_player, GridValue, GameState


class GameService:
    def __init__(self):
        # instantiate a game repository
        self.game_repository = GameRepository()

    def get_games(self):
        return self.game_repository.get_games()

    def get_game(self, game_id):
        return self.game_repository.get_game(game_id)

    def delete_game(self, game_id):
        return self.game_repository.delete_game(game_id)

    def update_game(self, game_id, modifiedGame):
        """
        finds the game to be updated,
        calls the validate_move functions
        and updates the board if move is validated

        Args:
            game_id (string): the game id
            modifiedGame (Game): the updated game Object

        Returns: tuple of game and message of update
            Game: returns updated game if update sucess otherwise returns None
            message: contains reason for invalidity if move could not be made
        """
        game = Game()
        unModifiedGame = self.game_repository.get_game(game_id)

        if unModifiedGame is None:
            return None, "Cannot get the game with specified game_id"
        modifiedGameBoard = modifiedGame.board

        # obtain the symbol the player is playing with, Naught or Cross
        player = unModifiedGame["player"]

        # validate move before updating
        is_valid, message = self.validate_move(modifiedGame, unModifiedGame, player)
        if not is_valid:
            return None, message
        else:

            gameWon = self.is_game_won(modifiedGameBoard, player)
            print("Game Won:", gameWon)

            # now make our own computer's move if the board is already not full
            if not self.is_board_filled(modifiedGameBoard):
                # set the computer's symbol to opposite of the player
                player = toggle_player(player)

                # make the move
                modifiedGameBoard = self.make_move(modifiedGameBoard, player)

                # check again, if the game is won after computer makes the move
                gameWon = self.is_game_won(modifiedGameBoard, player)
                print("Game Won: ", gameWon)

            game.set_game_id(game_id)
            game.set_board(modifiedGameBoard)
            if gameWon:
                game.set_status(f"{player}_WON")
            else:
                # the game is drawn if the board is full and nobody won
                if self.is_board_filled(modifiedGameBoard):
                    game.set_status(GameState.DRAW.value)

            # finally update the gameBoard
            self.game_repository.update_game(game_id, game)

            returned_game = self.game_repository.get_game(game_id)
            return returned_game, "Game updated"

    def start_game(self, board):
        """
        initialize game Data to start a game,
        after validating the sent board data
        and after checking if player has sent the board with its own move

        Args:
            board (string): the board data

        Returns:
            Game: returns if game could be started otherwise returns None
        """

        # initialize a game Object
        game = Game()

        boardData = list(board)

        # validate board
        if len(boardData) != 9:
            print("Invalid Board Data")
            return None
        game.set_board(board)

        # get the index and value of Board which are not Unfilled
        tup = [(i, s) for i, s in enumerate(boardData) if s != GridValue.Unfilled.value]

        if len(tup) == 1:
            # the case if player has sent board by making its move
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

            # add the game to database
            self.game_repository.add_game(game)

            return game.to_json()

        elif len(tup) == 0:
            # the case if game is started with no initial move
            # computer will make the first move

            # select a random symbol, Naught or Cross
            player = random.choice([GridValue.Cross.value, GridValue.Naught.value])
            computer = toggle_player(player)
            game.set_player(player)
            game.set_computer(computer)

            # make computer's move
            newGameData = self.make_move(boardData, computer)
            print(
                f"game initialized with player as: {player} and computer as: {computer}"
            )
            game.set_board(newGameData)

            # add the game to database
            self.game_repository.add_game(game)
            return game.to_json()

        else:
            print("Invalid Game Initialization")
            return None

    def validate_move(self, newGameData, oldGameData, player):
        """
        function that checks if the Board data sent by user is valid
        Validation list:
            check if the game is in running state or completed state
            check if the board string has exactly 9 characters
            check if there was exactly one move made
            check if there was any overriding of filled Grid in the board
            check if the newMove is made by the right symbol,
                if the player was playing with Naught, newMove should not be made with Cross


        Args:
            newGameData (dict): the modified Game Object
            oldGameData (dict): the original game Object
            player (char): the player's symbol, naught or cross

        Returns:
            (Validity, message) = returns True if valid and false , along with the message that may contain reason for invalidity

        """

        newBoard = newGameData["board"]
        oldBoard = oldGameData["board"]

        if oldGameData["status"] != GameState.RUNNING.value:
            # case to check if the game is in running state

            invalidation_reason = "Game is not in running state"
            print("Game is not running")
            return False, invalidation_reason

        if len(list(newBoard)) != 9:
            # case to check if the board string has exactly 9 characters
            invalidation_reason = "Grid Value length not equal to 9"
            print("Invalid Board Data")
            return False, invalidation_reason

        # Save the board data in set of tuples of the index and value of Filled Grid in board
        # Used this datastructure for conveniene to check for consecutive move
        newState = {(i, s) for i, s in enumerate(newBoard) if s in "XO"}
        oldState = {(i, s) for i, s in enumerate(oldBoard) if s in "XO"}

        if oldState <= newState:
            # the oldState set should be a subset of the newState set

            newMove = newState - oldState

            if len(newMove) != 1:
                # ensures there was just one move made
                return False, "More than one move made"
            if list(newMove)[0][1] != player:
                # ensures the newMove is made by the rightful symbol
                return False, "Player made the move with wrong symbol"
            else:
                return True, "Move validated"
        else:
            return False, "New Board data does not comply with old Board data"

    def make_move(self, board, computer):
        """
        Make Computer's move on one of the random unfilled grid of the board

        Args:
            board (string): the board
            computer (char): the player's symbol
        Returns:
            board (string): the new board data
        """

        if not self.is_board_filled(board):
            # check if the board is already full before making computer's move
            board = list(board)

            # the indices of grids which are unfilled
            unfilledIndices = [
                idx for idx, ele in enumerate(board) if ele == GridValue.Unfilled.value
            ]

            # choose a random position for the move from the list of unfilled indices
            randomInt = random.choice(unfilledIndices)

            board[randomInt] = computer

            # convert the board back to string from list
            board = "".join(map(str, board))

            return board
        else:
            # if board is full, return the same board
            return board

    def is_board_filled(self, board):
        """
        check if the board is completely full and does not have any unfilled grids

        Args:
            board (string): the board

        Returns:
            boolean: True is board is full, False otherwise
        """

        board = list(board)

        # check if there are any Unfilled grid in the board
        isFull = GridValue.Unfilled.value not in set(board)

        return isFull

    def is_game_won(self, board, player):
        """
        Check if the game is won

        Args:
            board (string): the board
            player (char): the player's symbol

        Returns:
            boolean: True if the game is won, False otherwise
        """
        # initialize to list of winningSets, which are the success cases
        # loaded from utils.py
        winSets = winningSets
        playersGrid = {idx for idx, ele in enumerate(board) if ele == player}

        return any(winSet <= playersGrid for winSet in winSets)
