# Aero_request
## Video Demonstration

![pygame window 2024-05-22 11-47-20 (online-video-cutter com) (2)](https://github.com/meriemjma/Aero_request/assets/130979570/c5ec806f-6e75-4697-847e-dca72f3dfa5c)



## How to Play

0. Make sure all libraries are installed (see setup section)
1. Navigate to the Aero_request directory: `cd Aero_request`
2. Run the `Play_aerorequest.py` script with the `-use` option:
    ```
    python Play_aerorequest.py -use
    ```
   - Controls:
     - W: Move the drone forward.
     - S: Move the drone backward.
     - A: Rotate the drone to the left.
     - D: Rotate the drone to the right.

## How To Use the Environment

0. Install the environment by running `pip install .` in the Aero_request directory.
1. Import the necessary modules:
    ```python
    import Aerorequest
    import gym
    ```
2. Use `gym.make(...)` to get an instance of the environment:
    ```python
    env = gym.make("Aerorequest_pixels_v0")  # Aerorequest with pixels as the observation space
    ```
    ```python
    env = gym.make("Aerorequest_features_v0")  # Aerorequest with features as the observation space
    ```
    Look at the signature of `__init__` of the `Aerorequest` class in `aerorequest.py` for more customization options.
