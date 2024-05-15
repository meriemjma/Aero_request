import os
import sys
from math import sin, cos, pi, sqrt
from random import randrange

import gym
import numpy as np
import pygame
from gym import spaces

current_dir = os.path.dirname(os.path.realpath(__file__))
env_dir = os.path.join(current_dir, 'env')
sys.path.append(env_dir)

from .Player import HumanPlayer


class Aerorequest(gym.Env):
    """
    Custom Gym environment for controlling a drone to reach a target.

    Parameters:
        render_mode (str): Rendering mode, either 'human' or 'rgb_array'.
        obs_type (str): Type of observation, either 'pixels' or 'features'.
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 24}

    def __init__(self, render_mode='human', obs_type='pixels'):
        """
        Initialize the Aerorequest environment.

        Args:
            render_mode (str): Rendering mode.
            obs_type (str): Type of observation.
        """

        # Calls the constructor of the superclass (gym.Env) to initialize the environment.
        super(Aerorequest, self).__init__()

        # Set observation type attribute
        self.obs_type = obs_type

        # Game constants
        self.FPS = self.metadata["render_fps"]
        self.WIDTH = 650
        self.HEIGHT = 650
        self.gravity = 0.08
        self.mass = 1  # Mass of the drone
        self.arm = 25  # Length of the arm of the drone
        self.time_limit = 100
        self.respawn_timer_max = 3

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Aerorequest Environment")
        self.FramePerSec = pygame.time.Clock()
        self.FramePerSec.tick(24)

        # Initialize player and target sprites
        self.load_sprites()

        # Initialize game variables
        self.time = 0
        self.step_count = 0

        # Initialize player
        self.player = HumanPlayer()

        # Define action space
        self.action_space = spaces.Discrete(4)

        # Define observation space based on observation type
        if obs_type == 'pixels':
            self.observation_space = spaces.Box(low=0, high=255, shape=(64, 64, 3), dtype=np.uint8)
        elif obs_type == 'features':
            self.observation_space = spaces.Dict({
                "player_position": spaces.Box(low=-100000, high=100000, shape=(2,), dtype=np.float32),#to fix
                "player_angle": spaces.Box(low=0, high=360, shape=(1,), dtype=np.float32),
                "target_position": spaces.Box(low=0, high=self.WIDTH, shape=(2,), dtype=np.float32),
                "score": spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32)
            })
        else:
            raise ValueError("Invalid observation type. Choose 'pixels' or 'features'.")

        # Set render mode
        self.render_mode = render_mode

        # Call reset to initialize the environment
        self.reset()

    def load_sprites(self):
        """
        Load player and target sprites.
        """
        # Loading player sprite
        self.player_width = 80
        player_image = pygame.image.load(os.path.join("C:\\Users\\Maryem\\Desktop\\Aero_request\\Aerorequest\\env\\ressources\\drone1.png"))
        self.player_image = pygame.transform.scale(player_image, (self.player_width, int(self.player_width * 0.30)))

        # Loading target sprite
        self.target_width = 50
        self.target_height = 50
        target_image = pygame.image.load(os.path.join("C:\\Users\\Maryem\\Desktop\\Aero_request\\Aerorequest\\env\\ressources\\target1.png"))
        self.target_image = pygame.transform.scale(target_image, (self.target_width, self.target_height))

        self.targets = [] # To store positions of target
        self.spawn_target()


    def spawn_target(self):
        """
        Spawn a new target.
        """
        self.targets = [(randrange(100, self.WIDTH - 100), randrange(100, self.HEIGHT - 100))]

    def spawn_player(self):
        """
        Respawn the player.
        """
        # Reset player position and state
        self.player.angle, self.player.angular_speed, self.player.angular_acceleration = 0, 0, 0
        self.player.x_position, self.player.x_speed, self.player.x_acceleration = self.WIDTH / 2, 0, 0
        self.player.y_position, self.player.y_speed, self.player.y_acceleration = self.HEIGHT / 2, 0, 0
        self.player.dead = False
        self.player.respawn_timer = 0

    def step(self, action):
        """
        Take a step in the environment.

        Args:
            action (int): Action taken by the agent.

        Returns:
            observation (object): Agent's observation of the current environment.
            reward (float): Reward from the previous action.
            done (bool): Whether the episode has ended
            info (dict): Additional information.(Positions and distance).
        """
        reward = 0.0  # to modify it later for RL agent
        done = False
        info = {}
        # Initialize thruster_left and thruster_right with default values
        thruster_left = self.player.thruster_mean
        thruster_right = self.player.thruster_mean
        if not self.player.dead:
            # Initialize accelerations
            x_acceleration = 0
            y_acceleration = self.gravity
            angular_acceleration = 0

            # Calculate propeller force based on action
            if action == 0:  # UP
                thruster_left = self.player.thruster_mean + self.player.thruster_amplitude
                thruster_right = self.player.thruster_mean + self.player.thruster_amplitude
            elif action == 1:  # DOWN
                thruster_left = self.player.thruster_mean - self.player.thruster_amplitude
                thruster_right = self.player.thruster_mean - self.player.thruster_amplitude
            elif action == 2:  # LEFT
                thruster_left = self.player.thruster_mean - self.player.diff_amplitude
                thruster_right = self.player.thruster_mean
            elif action == 3:  # RIGHT
                thruster_left = self.player.thruster_mean
                thruster_right = self.player.thruster_mean - self.player.diff_amplitude

            # Calculate accelerations according to Newton's laws of motion
            x_acceleration += (
                    -(thruster_left + thruster_right) * sin(self.player.angle * pi / 180) / self.mass
            )
            y_acceleration += (
                    -(thruster_left + thruster_right) * cos(self.player.angle * pi / 180) / self.mass
            )
            angular_acceleration += self.arm * (thruster_right - thruster_left) / self.mass

            # Update Player speed
            self.player.x_speed += x_acceleration
            self.player.y_speed += y_acceleration
            self.player.angular_speed += angular_acceleration

            # Update Player position
            self.player.x_position += self.player.x_speed
            self.player.y_position += self.player.y_speed
            self.player.angle += self.player.angular_speed

            # Calculate distance to target
            dist = sqrt((self.player.x_position - self.targets[0][0]) ** 2 +
                        (self.player.y_position - self.targets[0][1]) ** 2)

            # If target reached, respawn target and update score
            if dist < 50:
                self.spawn_target()
                self.score += 10  # Increase score when target reached

            # If too far, die and respawn after timer
            elif dist > 1000:
                self.player.dead = True
                self.player.respawn_timer = self.respawn_timer_max
        else:
            # Decrement respawn timer and respawn if timer reaches 0
            self.player.respawn_timer -= 1 / self.FPS
            if self.player.respawn_timer < 0:
                self.spawn_player()
                info['status'] = 'Player died'

        # Check if game is over
        if self.time >= self.time_limit:
            # Game over, reset time and end game
            self.time = 0
            done = True
            info['status'] = 'Time Limit Exceeded.. will start new Episode'
            self.reset()  # Reset the environment

        # Increment time
        self.time += 1 / self.FPS

        # Update step count
        self.step_count += 1

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, done, False, info

    def render(self, mode='human'):
        """
        Render the environment.

        Args:
            mode (str): Rendering mode, either 'human' or 'rgb_array'.

        Returns:
            (object or np.array): Rendered image or array.
        """
        if mode == 'human':
            # Display environment in a Pygame window
            self._render_human()
        elif mode == 'rgb_array':
            # Render environment as an RGB array
            return self._render_rgb_array()

    def _render_human(self):
        """
        Render the environment in human mode.
        """
        # Display background
        self.screen.fill((131, 176, 181))

        # Render player
        player_copy = pygame.transform.rotate(self.player_image, self.player.angle)
        self.screen.blit(
            player_copy,
            (
                self.player.x_position - int(player_copy.get_width() / 2),
                self.player.y_position - int(player_copy.get_height() / 2),
            ),
        )

        # Render target
        target_pos = (
            self.targets[0][0] - int(self.target_image.get_width() / 2),
            self.targets[0][1] - int(self.target_image.get_height() / 2)
        )  # Calculate the position to draw the target sprite
        self.screen.blit(self.target_image, target_pos)

        # Render time and score on the left side
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Time: {int(self.time)}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))  
        self.screen.blit(time_text, (20, 20))
        self.screen.blit(score_text, (20, 60))

        pygame.display.update()
        self.FramePerSec.tick(self.FPS)


    def _render_rgb_array(self):
        """
        Render the environment as an RGB array.

        Returns:
            np.array: Rendered image as an RGB array.
        """

        surface = pygame.surfarray.array3d(self.screen)
        return surface

    def reset(self):
        """
        Reset the environment.

        Returns:
            tuple: Initial observation of the environment and additional information.
        """
        self.spawn_player()

        # Reset targets and score
        self.targets = []
        self.spawn_target()
        self.score = 0

        # Reset time and step count
        self.time = 0
        self.step_count = 0

        # Get observation and info
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, info

    def _get_obs(self):
        """
        Get the observation of the environment.

        Returns:
            np.array or dict: Observation of the environment based on the observation type.
        """
        if self.obs_type == 'pixels':
            # Render the environment to get the observation
            observation = self._render_rgb_array()
            # Convert the observation to a surface
            observation_surface = pygame.surfarray.make_surface(observation)
            # Resize the surface
            observation_resized = pygame.transform.scale(observation_surface, (64, 64))
            # Convert the resized surface back to a numpy array
            observation_resized_np = pygame.surfarray.array3d(observation_resized)
            return observation_resized_np
        elif self.obs_type == 'features':
            # Construct observation dictionary
            observation = {
                "player_position": np.array([self.player.x_position, self.player.y_position], dtype=np.float32),
                "player_angle": np.array([self.player.angle], dtype=np.float32),
                "target_position": np.array(self.targets[0], dtype=np.float32),
                "score": np.array([self.score], dtype=np.float32)
            }
            return observation

    def _get_info(self):
        """
        Get additional information about the environment.

        Returns:
            dict: Dictionary containing the distance between the agent and the target.
        """
        agent_pos = np.array([self.player.x_position, self.player.y_position])
        target_pos = np.array(self.targets[0])
        distance = np.linalg.norm(agent_pos - target_pos, ord=1)
        return {"distance": distance}

    def close(self):
        """
        Close the Pygame window.
        """
        pygame.quit()

