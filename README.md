# Battleship — Terminal-Based Strategy Game

A Python implementation of the classic Battleship strategy game played via the command line interface (CLI). The project features interactive human-vs-bot gameplay, custom ship placement validation, a targeted bot decision algorithm, and game state persistence via CSV data logging.

---

## Technical Overview

- **Language:** Python 3.x
- **User Interface:** Command Line Interface (CLI)
- **Data Persistence:** CSV file storage (`player_ships.csv`, `bot_ships.csv`, `game_state.csv`)
- **Key Algorithms:** Custom grid coordinate validation, non-adjacent placement logic, stateful bot targeting AI

---

## Project Structure

```text
battleship/
├── data/
│   ├── player_ships.csv      # Player fleet layout and coordinates
│   ├── bot_ships.csv         # Bot fleet layout and coordinates
│   └── game_state.csv        # Logged game actions, hits, and misses
├── src/
│   ├── ship_input.py         # Player ship placement and input parsing
│   ├── bot_generation.py     # Procedural bot fleet placement
│   ├── gameplay.py           # Core game loop, turn mechanics, and win conditions
│   └── utils.py              # Grid rendering and validation helper functions
├── outputs/                  # Execution logs and output records (optional)
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

```
## System Architecture & Game Design
Fleet Composition & Placement Rules
The game is played on a 10×10 grid. Each player commands a fleet consisting of 10 ships:

1x Battleship (Size 4)

2x Cruisers (Size 3)

3x Destroyers (Size 2)

4x Submarines (Size 1)

Ships are represented as lists of coordinate tuples (x, y). Placement validation ensures that no two ships overlap or touch each other, including diagonal adjacencies.


## Artificial Intelligence Strategy
The opponent bot executes an adaptive shooting algorithm:

1. Random Search: Fires randomly across unvisited grid coordinates.

2. Target Tracking: Upon recording a hit, switches to adjacent cell investigation.

3. Axis Locking: Locks onto a vertical or horizontal axis after two consecutive hits to systematically sink the targeted ship.

4. Auto-Clearing: Automatically marks all perimeter cells surrounding a destroyed ship as misses.


## Setup and Execution
1. Installation
Clone the repository and navigate to the project directory:

```
git clone <repository-url>
cd battleship
```
Install dependencies (if required):
```
pip install -r requirements.txt
```

2. Running the Game
Launch the game loop from the root directory:

```
python3 main.py
```


## Gameplay Guide
1. Fleet Setup
Input coordinates for each ship sequentially in space-separated x y pairs.

Example for a Size 3 Cruiser:
```
0 0 0 1 0 2
```

### 2. Game Loop & Interface
During each turn, two 10×10 grids are rendered:

Player Board: Displays your fleet, opponent shots, and hits.

Bot Board: Displays your target history (hits and misses).

Board legend:

. — Unexplored / Empty cell

X — Successful hit

O — Missed shot

Input target coordinates during your turn using the x y format until one fleet is entirely eliminated.
