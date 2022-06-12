
import numpy as np
import random
from Model.Game import GridValue, State


nRows = 3
nCols = 3
DRAW = "GAME DRAW"



#use if necessary to toggle player
def togglePlayer(player):
    player = 'O' if player == 'X' else 'X'
    return player


#initialize game Data after first post request to start a game
#This is called upon post request to start the game
#TODO: might need to change datatype switch between oneD or 2D data
def initializeGameData(gameData):
    global player
    global computer
    
    oneDGameData = gameData.flatten()
    tup =  ([(i,s) for i,s in enumerate(oneDGameData) if s != '-'])
    print(tup)
    if (len(tup) == 1):
        player = tup[0][1]
        computer = togglePlayer(player)
        print(f"game initialized by player {player}")
        return gameData
    elif (len(tup) == 0):
        print("Game started with no initial move: ---------")
        print("Computer will make the first move")
        #TODO: randomly select player
        player = random.choice([GridValue.Cross.value, GridValue.Naught.value])
        computer = togglePlayer(player)
        newGameData=makeMove(gameData,computer)
        return newGameData
    else:
        print("Invalid Game Initialization")
        return False


def main():

    #initialize the game data as numpy array of 3 rows and 3 columns for new board
    gameData = np.full((nRows, nCols), GridValue.Unfilled.value)
    print(gameData)
    #testcases for gameData
    # gameData = np.array([['X','O','-'],['-','X','-'],['-','O','X']]) #diagonal
    # gameData = np.array([['X','O','-'],['-','O','O'],['X','X','X']]) #row
    # gameData = np.array([['X','O','-'],['X','X','-'],['X','O','O']]) #column
    # gameData = np.array([['-','O','X'],['-','X','-'],['X','O','-']]) #antidiagonal
    gameData = np.array([['O','X','O'],['O','X','O'],['X','O','O']]) #allGridFilled
    print("GameData:\n", gameData)

    #TODO: change which player is making the move
    #random initialization
    player = 'X'
    computer = 'O'

    #initializeGameData
    #testCase for initializeGame
    gameData =  np.array([['-','-','-'],['-','-','-'],['-','-','-']]) # all empty, fresh game
    gameData =  np.array([['-','-','-'],['-','X','-'],['-','-','-']]) # only one element X at position 4
    gameData =  np.array([['-','-','-'],['-','O','-'],['-','-','-']]) # only one element O at position 4
    # gameData =  np.array([['-','-','-'],['-','X','O'],['-','-','-']]) # invalid game initialization
    initializeGameData(gameData)

    # # TODO: while(not isBoardFilled(gameData)):
    # gameData = makeMove(gameData,player)
    # #call the function which checks if there are success cases in the Game Data
    # isWon = isGameWon(gameData,player)
    # if(not isWon and isBoardFilled(gameData)):
    #     print(DRAW)

    #Test case for validate move
    # oldgameData = np.array([['X','O','-'],['-','O','O'],['X','X','-']])
    # newGameData = np.array([['X','O','X'],['-','O','O'],['X','X','-']]) #valid  ->X moves at position 2
    # newGameData = np.array([['X','O','O'],['-','O','O'],['X','X','-']]) #invalid case , but player's turn was X, but changed to O -> O moves at position 2
    # newGameData = np.array([['X','X','-'],['-','O','O'],['X','X','-']]) #invalid case because old data -> X overrides O at position 1
    # validated = validateMove(newGameData, oldgameData, player)
    # print("Move validated:", validated)


  


def isGameWon(gameData,player):
    SUCCESS = f'Game won by Player {player}'
    
    #Check for row Value success
    for i in range(nRows):
        #The Data cannot be unfilled
        if gameData[i][0]!=GridValue.Unfilled.value and np.all(gameData[i]==gameData[i][0]):
            print(SUCCESS)
            return True
    
    #Check for column value success
    gameDataTransposed = gameData.T
    for i in range(nRows):
        if gameDataTransposed[i][0]!=GridValue.Unfilled.value and np.all(gameDataTransposed[i]==gameData[i][0]):
            print(SUCCESS)
            return True

    # Check for diagonal success
    gameDataDiagonal = gameData.diagonal()
    for i in range(nRows):
        if gameDataDiagonal[0]!=GridValue.Unfilled.value and np.all(gameDataDiagonal == gameDataDiagonal[0]):
            print(gameDataDiagonal)
            print(SUCCESS)
            return True

    #Check for antiDiagonal success
    gameDataAntiDiagonal = np.fliplr(gameData).diagonal()

    for i in range(nRows):
        if gameDataAntiDiagonal[0]!=GridValue.Unfilled.value and np.all(gameDataAntiDiagonal == gameDataAntiDiagonal[0]):
            print(gameDataAntiDiagonal)
            print(SUCCESS)
            return True
    
    #Game is drawn if board is full and none of the above success criteria is met, but 
    return False
    

def makeMove(gameData, player):

    if not isBoardFilled(gameData):
        oneDGameData = gameData.flatten()
        print("One D Game Data", oneDGameData)
        unfilledIndices = np.where(oneDGameData == GridValue.Unfilled.value)[0]
        print("Unfilled:", unfilledIndices)
        randomInt = np.random.choice(unfilledIndices)
        print("Grid position for new move", randomInt)
        gameData.flat[randomInt] = player
        print("New Game Data\n",gameData)
        return gameData
    else:
        return gameData
        



def isBoardFilled(gameData):
    isFull = not np.any(gameData == GridValue.Unfilled.value)
    print("isFull",isFull)
    return isFull


def validateMove(newGameData, oldGameData, player):
    if(len(newGameData)!=9):
        print("Invalid Board Data")
        return False
    # newOneDGameData = newGameData.flatten()
    newState = ({(i,s) for i,s in enumerate(newGameData) if s in 'XO'})
    # oldOneDGameData = oldGameData.flatten()
    oldState = ({(i,s) for i,s in enumerate(oldGameData) if s in 'XO'})
    print("oldState", oldState)
    print("newState", newState)
    if(oldState <= newState):
        newMove = newState - oldState
        print("newMove", newMove)
        return len(newMove) == 1 and list(newMove)[0][1] == player
    else:
        return False



main()


