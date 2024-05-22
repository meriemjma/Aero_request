import pygame
import gym
from Aerorequest.env.Player import HumanPlayer

def main():
    """
    Main function to initialize the game environment and start the game loop.
    """
    env = gym.make('Aerorequest_pixels_v0', render_mode="human")
    human_player = HumanPlayer()
    observation, info = env.reset()

    # Game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()   

        # Get actions for the player
        action = human_player.get_keyboard_actions()

        # Call step method to update player position
        observation, reward, terminated, truncated, info = env.step(action)

        # Print observation and info to the console
        # print("Observation:", observation)
        # print("Info:", info)

        if terminated or truncated:
            observation, info = env.reset()

if __name__ == "__main__":
    main()
