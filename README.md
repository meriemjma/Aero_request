# Aero_request
## Video Demonstration

![Aerorequest Video Demonstration]([https://drive.google.com/uc?export=download&id=1lcrKSVlChxLouXsiahOHVl-hDnRWI8SD](https://drive.google.com/file/d/1lcrKSVlChxLouXsiahOHVl-hDnRWI8SD/view?usp=sharing))
## How to Play

0. Make sure all libraries are installed (see setup section)
1. Navigate to the Aero_request directory: `cd Aero_request`
2. Run the `Play_aerorequest.py` script with the `-use` option:
    ```
    python Play_aerorequest.py -use
    ```
   - Controls:
     - Up arrow key: Move the drone forward.
     - Down arrow key: Move the drone backward.
     - Left arrow key: Rotate the drone counter-clockwise.
     - Right arrow key: Rotate the drone clockwise.

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
