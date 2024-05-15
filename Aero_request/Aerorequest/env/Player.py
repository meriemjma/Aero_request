import pygame

class Player:
    """
    Base class representing a player in the game.
    """

    def __init__(self):
        """
        Initialize player attributes.
        """
        self.thruster_mean = 0.04
        self.thruster_amplitude = 0.04
        self.diff_amplitude = 0.003
        self.angle, self.angular_speed, self.angular_acceleration = 0, 0, 0
        self.x_position, self.x_speed, self.x_acceleration = 400, 0, 0
        self.y_position, self.y_speed, self.y_acceleration = 400, 0, 0
        self.target_counter = 0
        self.dead = False
        self.respawn_timer = 3

class HumanPlayer(Player):
    """
    Class representing a human player in the game, inheriting from Player class.
    """

    def __init__(self):
        """
        Initialize human player attributes.
        """
        self.name = "Human"
        self.alpha = 255
        super().__init__()

    def get_keyboard_actions(self):
        """
        Get the current action based on keyboard input.
        
        Returns:
            int: Action corresponding to the pressed key.
        """
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[pygame.K_UP]:
            return 0
        elif pressed_keys[pygame.K_DOWN]:
            return 1
        elif pressed_keys[pygame.K_LEFT]:
            return 2
        elif pressed_keys[pygame.K_RIGHT]:
            return 3
        
        
        return -1  

