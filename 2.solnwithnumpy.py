from enum import Enum
import numpy as np

#class for enum to identify unfilled value, cross and naught values
class GridValue(Enum):
    Unfilled = 0
    Cross = 1
    Naught = 2

nRows = 3
nCols = 3


def main():

    #initialize the game data as numpy array of 3 rows and 3 columns for new board
    gameData = np.zeros((nRows, nCols))
    #testcases for gameData
    # gameData = np.array([[1,2,0],[0,1,0],[0,2,1]]) #diagonal
    # gameData = np.array([[1,2,0],[0,1,0],[1,1,1]]) #row
    # gameData = np.array([[1,2,0],[1,1,0],[1,2,1]]) #column
    gameData = np.array([[0,2,1],[0,1,0],[1,2,0]]) #antidiagonal
    # gameData = np.array([[2,1,2],[2,1,2],[1,2,2]]) #allGridFilled
    print("GameData:\n", gameData)

    player = 1 #TODO: change which player is making the move

    # TODO: while(not isBoardFilled(gameData)):
    gameData = makeMove(gameData,player)
    #call the function which checks if there are success cases in the Game Data
    isGameWon(gameData,player)

  



def isGameWon(gameData,player):
    SUCCESS = f'Game won by Player {player}'
    #Check for row Value success
    for i in range(nRows):
        #The Data cannot be unfilled
        if gameData[i][0]!=GridValue.Unfilled and np.all(gameData[i]==gameData[i][0]):
            print(SUCCESS)
            return True
    
    #Check for column value success
    gameDataTransposed = gameData.T
    for i in range(nRows):
        if gameDataTransposed[i][0]!=GridValue.Unfilled and np.all(gameDataTransposed[i]==gameData[i][0]):
            print(SUCCESS)
            return True

    # Check for diagonal success
    gameDataDiagonal = gameData.diagonal()
    for i in range(nRows):
        if gameDataDiagonal[0]!=GridValue.Unfilled and np.all(gameDataDiagonal == gameDataDiagonal[0]):
            print(gameDataDiagonal)
            print(SUCCESS)
            return True

    #Check for antiDiagonal success
    gameDataAntiDiagonal = np.fliplr(gameData).diagonal()

    for i in range(nRows):
        if gameDataAntiDiagonal[0]!=GridValue.Unfilled and np.all(gameDataAntiDiagonal == gameDataAntiDiagonal[0]):
            print(gameDataAntiDiagonal)
            print(SUCCESS)
            return True

def makeMove(gameData, player):
    if not isBoardFilled(gameData):
        oneDGameData = gameData.flatten()
        zeroIndices = np.where(oneDGameData ==0)[0]
        print(zeroIndices)
        randomInt = np.random.choice(zeroIndices)
        print("Grid position for new move", randomInt)
        gameData.flat[randomInt] = player
        print("New Game Data\n",gameData)
        return gameData
        

def isBoardFilled(gameData):
    print(np.all(gameData))

main()


