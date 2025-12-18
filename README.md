# Battleship Final Project:<3

This is a simplified version of the classic Battleship game implemented in Python.  
The game is played in the terminal and allows a player to play against a bot.

---

## Project Structure

├─ main.py
├─ data/
│ ├─ player_ships.csv
│ ├─ bot_ships.csv
│ └─ game_state.csv
├─ src/
│ ├─ ship_input.py # Player ship input
│ ├─ bot_generation.py # Bot ship generation
│ ├─ gameplay.py # Game loop and logic
│ └─ utils.py # Helper functions
├─ outputs/ # Any logs or results (optional)
├─ requirements.txt
└─ README.md

--------------


## How to Play

1. Run the game:

```bash
python3 main.py
```


2. Player Ship Input

You will be asked to input your ships one by one:

Format example for size 3: 0 0 0 1 0 2 (space-separated x y pairs)

Ship sizes: 4, 3, 3, 2, 2, 2, 1, 1, 1, 1

Ships cannot touch each other, even diagonally.


3. Bot Ship Generation
The bot automatically generates valid ships following the same rules.


4. Game Loop

After both ship layouts are ready, the game starts.

You will see two boards:

Your board — shows your ships and bot hits.

Bot board — shows your hits and misses on the bot.

Enter your shots in x y format.

The game continues until all ships of one side are destroyed.


5. Game State CSV

The file data/game_state.csv keeps track of moves, hits, and misses.


---------------


LETS TALK ABT DESIGN PART:

Ships are represented as lists of coordinates (x, y).

Boards are 10x10, using . for empty, X for hits, O for misses.

Bot AI:

Random shooting initially.

Smart follow-up after a hit.

Axis locking after second consecutive hit.

Surrounding cells of destroyed ships are automatically marked as miss.


-----------------
Enjoy :3