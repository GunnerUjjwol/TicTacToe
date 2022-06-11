from flask import Flask
app = Flask(__name__)




@app.get('/hello/')
def welcome():
    return "Welcome to the game!"

@app.get('/games/')
def getAllGames():
    return f"All Games loaded", 200

@app.post('/games')
def startGame(gameData):
    return f"Game started with gameData: {gameData}"

@app.get('/games/<string:game_id>')
def getGame(game_id):
    return f"Game {game_id} loaded"

@app.put('/games/<string:game_id>')
def newMove(game_id):
    return f"Game {game_id} : New Move"

@app.delete('/games/<string:game_id>')
def deleteGame(game_id):
    return f"Game {game_id} : Deleted"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)