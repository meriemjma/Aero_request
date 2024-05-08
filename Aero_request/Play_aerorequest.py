import os
import sys
import pygame
from Aerorequest.env.aerorequest import Aerorequest
from Aerorequest.env.Player import HumanPlayer  # Import HumanPlayer class

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    env_dir = os.path.join(current_dir, 'Aerorequest', 'env')
    sys.path.append(env_dir)

    # Create the Aerorequest environment
    env = Aerorequest()

    # Load player and target sprites
    env.load_sprites()

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()  # Close the Pygame window
                sys.exit()

        # Get actions for the player
        if isinstance(env.player, HumanPlayer):
            action = env.player.get_keyboard_actions()
        else:
            # Logic for other types of players (not human)
            action = []

        # Call step method to update player position
        env.step(action)

        # Render the environment
        env.render()


if __name__ == "__main__":
    main()
