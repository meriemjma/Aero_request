import gym
from gym.utils.play import play
from Aerorequest.env import aerorequest

if __name__ == "__main__":
    # Create the Aerorequest environment with rgb_array render mode
    env = gym.make('Aerorequest_pixels_v0', render_mode="rgb_array")

    # Define the keys to actions mapping
    keys_to_actions = {
        "w": 0,
        "s": 1,
        "a": 2,
        "d": 3,
    }

    # Start the game loop
    play(env, keys_to_action=keys_to_actions, noop=None)
