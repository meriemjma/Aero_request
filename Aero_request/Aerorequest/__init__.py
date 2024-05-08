import gym
from gym.envs.registration import register
import sys
sys.path.append("C:\\Users\\Maryem\\Desktop\\Aero_request")

# Register environment version with pixel observations
register(
    id="Aerorequest_pixels_v0",
    entry_point="Aerorequest.env.aerorequest:Aerorequest",
    kwargs={'obs_type': 'pixels'}
)

# Register environment version with feature observations
register(
    id="Aerorequest_features_v0",
    entry_point="Aerorequest.env.aerorequest:Aerorequest",
    kwargs={'obs_type': 'features'}
)

# Create environments
env = gym.make('Aerorequest_pixels_v0')
env1 = gym.make('Aerorequest_features_v0')
