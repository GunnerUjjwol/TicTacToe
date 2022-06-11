from enum import Enum

#class for enum to identify unfilled value, cross and naught values
class GridValue(Enum):
    Unfilled = 0
    Cross = 1
    Naught = 2


def main():
    nRows = 3
    nCols = 3

    #initialize the game data as 2D array of 3 rows and 3 columns for new board
    gameData = [ [0]*3 for i in range(3)]

    #testcase for gameData
    gameData = [[1,2,0],[0,1,0],[0,2,1]]

    print(gameData)

    for i in range(nRows):
        for j in range(nCols):
            currentGrid = gameData[i][j]
            if(currentGrid==GridValue.Unfilled):
                #skip processing in this state if the currentData is Unfilled
                continue
            else:
                print(currentGrid)
                nextGrid = gameData[i][j+1]



main()


