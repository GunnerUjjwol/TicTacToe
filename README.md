TicTacToe 
============================

> TicTacToe game flask backend app with python

#### How to Run

Install all the dependencies in requirements.txt
```
pip install -r requirements.txt
```

Run the app.py script
```
python app.py
```

#### Code Structure

The backend is structured in Model, Service and Repository Model

```
|   app.py                      #the entrypoint of the APIs    
|   requirements.txt            #the list of dependencies to be installed
|   
+---Model
|   |   Game.py                 #The Game Model
|           
+---Repository
|   |   GameRepository.py       #Database for Games Dictionary and CRUD operations on them
|           
+---Service
|   |   GameService.py          #The Main Logic for the game
|           
\---Utils
    |   utils.py                #Utility Functions and variables
```
#####About the Game
The description of the game can be found at tictactoe.txt

#####About the API documentation
The API endpoint documentations can be found at tictactoe.yaml