from Repository.GameRepository import GameRepository
import random
from Model.Game import Game,GridValue, State
from Utils.utils import *
class GameService:

    DRAW = "GAME DRAW"

    def __init__(self):
        self.gameRepository = GameRepository()
        self.nRows = 3
        self.nCols = 3
        

    def get_games(self):
        return self.gameRepository.get_games()

    def get_game(self, game_id):
        return self.gameRepository.get_game(game_id)

    def delete_game(self, game_id):
        return self.gameRepository.delete_game(game_id)

    def update_game(self, game_id, modifiedGame):
        game = Game()
        unModifiedGame = self.gameRepository.get_game(game_id)

        if unModifiedGame is None:
            return False
        print("Found Game", unModifiedGame)
        #oldGameBoard = list(unModifiedGame['board'])
        oldGameBoard = unModifiedGame['board']
        modifiedGameBoard = modifiedGame.board
        
        
        print("OldGameData", oldGameBoard)
        #TODO: set the player who is playing now
        player = 'O'
        # validate move
        print(modifiedGameBoard)
        if(not self.validateMove(modifiedGame,unModifiedGame,player)):
            return "Bad Request", 400
        else:
            
            gameWon = self.isGameWon(modifiedGameBoard, player)
            print("Game Won", gameWon)
            
            

            #TODO: update in repo
            #GAMES = [modifiedGame if game['game_id'] == unModifiedGame['game_id'] else game for game in GAMES]

            #TODO: now make our own computer's move if the board is already not full, otherwise return status
            if(not self.isBoardFilled(modifiedGameBoard)):
                #TODO: might need to remove toggling computer
                player = togglePlayer(player)
                modifiedGameBoard = self.makeMove(modifiedGameBoard, player)
                
                #check again, if the game is won after computer makes the move
                gameWon = self.isGameWon(modifiedGameBoard,player)
                print("Game Won", gameWon)
                print(modifiedGameBoard)

            game.set_game_id(game_id)
            game.set_board(modifiedGameBoard)
            if(gameWon):
                game.set_status(f'{player}_WON')
            else:
                if (self.isBoardFilled(modifiedGameBoard)):
                    game.set_status('DRAW')
            self.gameRepository.update_game(game_id,game)



            returned_game = self.gameRepository.get_game(game_id) #change this after reflecting computers move
            return returned_game, 200
        

        


  
    #initialize game Data after first post request to start a game
    #This is called upon post request to start the game
    #TODO: might need to change datatype switch between oneD or 2D data  
    def startGame(self, board):
        game = Game()
        
        gameData = list(board)
        #validate board
        if(len(gameData)!=9):
            print("Invalid Board Data")
            return False
        game.set_board(board)
        tup =  ([(i,s) for i,s in enumerate(gameData) if s != '-'])
        print(tup)
        if (len(tup) == 1):
            player = tup[0][1]
            computer = togglePlayer(player)
            game.set_player(player)
            game.set_computer(computer)
            print(f"game initialized with player as: {player} and computer as: {computer}")
            self.gameRepository.add_game(game)            
            return game
            
        elif (len(tup) == 0):
            print("Game started with no initial move: ---------")
            print("Computer will make the first move")
            
            player = random.choice([GridValue.Cross.value, GridValue.Naught.value])
            computer = togglePlayer(player)
            game.set_player(player)
            game.set_computer(computer)
            print(game.__dict__)          
            newGameData=self.makeMove(gameData,computer)
            print(f"game initialized with player as: {player} and computer as: {computer}")
            self.gameRepository.add_game(game)
            return game
            
        else:
            print("Invalid Game Initialization")
            return False


     
    # define validation function
    def validateMove(self,newGameData, oldGameData, player):
        print(newGameData)
        print(oldGameData)
        newBoard = newGameData['board']
        oldBoard = oldGameData['board']
        if(oldGameData['status']!='RUNNING'):
            print("Game Already Complete")
            return False
        if(len(list(newBoard))!=9):
            print("Invalid Board Data")
            return False
        # newOneDGameData = newGameData.flatten()
        newState = ({(i,s) for i,s in enumerate(newBoard) if s in 'XO'})
        # oldOneDGameData = oldGameData.flatten()
        oldState = ({(i,s) for i,s in enumerate(oldBoard) if s in 'XO'})
        print("oldState", oldState)
        print("newState", newState)
        if(oldState <= newState):
            newMove = newState - oldState
            print("newMove", newMove)
            return len(newMove) == 1 and list(newMove)[0][1] == player
        else:
            return False
   
 
    def makeMove(self,gameData, player):
       
        if not self.isBoardFilled(gameData):
            # oneDGameData = gameData.flatten()
            gameData = list(gameData)
            print("One D Game Data", gameData)
            #unfilledIndices = np.where(gameData == GridValue.Unfilled.value)[0]
            unfilledIndices = [idx for idx,ele in enumerate(gameData) if ele == GridValue.Unfilled.value]
            print("Unfilled:", unfilledIndices)
            randomInt = random.choice(unfilledIndices)
            print("Grid position for new move", randomInt)
            gameData[randomInt] = player
            gameData = ''.join(map(str, gameData))
            print("New Game Data\n",gameData)
            return gameData
        else:
            return gameData
            



    def isBoardFilled(self,gameData):
        print("GridValue",GridValue.Unfilled.value)
        
        gameData= list(gameData)
        print(gameData)
        print(set(gameData))
        # isFull = not any(ele == GridValue.Unfilled.value for ele in enumerate(gameData))
        isFull =  (GridValue.Unfilled.value not in set(gameData))
        
        print("isFull",isFull)
        return isFull    


    def isGameWon(self,board, player):
        winningSets = [
            # row Match Indices
            {0,1,2}, {3,4,5}, {6,7,8},
            #column Match Indices
            {0,3,6}, {1,4,7}, {2,5,8},
            #diaganoal Match indices
            {0,4,8}, {2,4,6}
        ]
        print("Board",board)
        playersGrid = {idx for idx,ele in enumerate(board) if ele == player}
        
        print(playersGrid)
        return any( winSet <= playersGrid for winSet in winningSets)

