# main.py

from src import ship_input, bot_generation, gameplay

def main():
    """
    Main entry point for Battleship game.
    Steps:
    1. Player inputs ships
    2. Bot generates ships
    3. Game loop starts
    """
    ship_input.run_ship_input()

    bot_generation.run_bot_generation()

    gameplay.run_game()


if __name__ == "__main__":
    main()
