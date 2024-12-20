import gym  # Import the OpenAI Gym library for environment creation
import wandb  # Import the Weights and Biases library for logging (optional, currently unused)
from gym import spaces  # Import spaces for defining action and observation spaces
from math import sin, cos, pi, acos, radians, degrees, exp, pow  # Import mathematical functions
import numpy as np  # Import NumPy for numerical operations
import time  # Import time for managing delays and ticks
import pandas as pd  # Import pandas for handling logs and dataframes
from statistics import mean  # Import mean calculation from statistics module
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

# Define constants for the state space
NUM_OBS = 6  # Number of observations
MAX_YAW = 2 * pi  # Maximum yaw angle (radians)
MAX_T = 130  # Maximum time
MAX_R = 2  # Maximum yaw rate (radians/second)
MAX_S = 800  # Maximum longitudinal position
MAX_L = 6  # Maximum lateral position
MAX_VX = 150  # Maximum longitudinal velocity
MAX_VY = 80  # Maximum lateral velocity
MAX_ACC = 20  # Maximum acceleration
MAX_STEER = 90  # Maximum steering angle (degrees)

MIN_S = 0  # Minimum longitudinal position
MIN_L = -6  # Minimum lateral position
MIN_VX = 0  # Minimum longitudinal velocity
MIN_VY = -80  # Minimum lateral velocity
MIN_YAW = -2 * pi  # Minimum yaw angle
MIN_R = -2  # Minimum yaw rate

# Define constants for the reward system
R_OOB = 5000  # Reward for successfully completing the episode
R_OOF = -500  # Penalty for going out of bounds
R_OOT = 0  # Reward for other situations

# Define a helper constant
PI_2 = 2 * pi  # Two times pi

# Define the custom environment class
class Drift_env(gym.Env):
    metadata = {'render.modes': ['gui', 'none']}  # Metadata for rendering modes

    def __init__(self, world, v_ini, L_road, max_episode_iters=1000):
        """
        Initialize the environment.

        Args:
            world: Simulation world instance.
            v_ini: Initial velocity.
            L_road: Lateral road tolerance.
            max_episode_iters: Maximum number of iterations per episode.
        """
        self._world = world
        self.v_ini = v_ini
        self.py_tol = L_road

        # Define action space: [steering, throttle]
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))

        # Define observation space: [vx, vy, yaw, r, px, py]
        self.observation_space = spaces.Box(low=-1, high=1, shape=(NUM_OBS,))

        # Define observation range
        self._obs_max_vals = np.array([MAX_S, MAX_L, MAX_VX, MAX_VY, MAX_YAW, MAX_R])
        self._obs_min_vals = np.array([MIN_S, MIN_L, MIN_VX, MIN_VY, MIN_YAW, MIN_R])

        # Initialize variables for tracking state and rewards
        self._velocity = None
        self._delta_phi = None
        self._reward = None
        self._py = None

        # Episode management
        self.max_episode_iters = max_episode_iters
        self.iters = 0
        self.global_tick = 0

        # Logging data
        self.ticks = []
        self.rewards = []
        self.velocities = []

        # Recent values for smoothing logs
        self.last_10_betas = []
        self.last_10_epsilons = []
        self.last_10_rewards = []
        self.last_10_velocities = []

        # Training mode flag
        self.is_training = False
        self.control = []
        self._action1 = [1, 1]

        # Reset the environment
        self.reset()

    def log(self):
        """ Log the recent rewards and velocities. """
        self.last_10_rewards.append(self._reward)
        self.last_10_velocities.append(self._velocity)

        if len(self.last_10_betas) == 10:
            self.ticks.append(self.global_tick)

            self.rewards.append(mean(self.last_10_rewards))
            self.velocities.append(mean(self.last_10_velocities))

            self.last_10_rewards = []
            self.last_10_velocities = []

    def plot_logs(self):
        """ Plot the logged rewards and velocities over time. """
        vals = [self.rewards, self.velocities]
        names = ["Reward", "Velocity"]

        for i in range(2):
            t = self.ticks
            s = vals[i]
            name = names[i]

            fig, ax = plt.subplots()
            ax.plot(t, s)
            ax.set(xlabel='Timestep', title=name)
            ax.grid()

            fig.savefig(name + ".png")

    def save_logs(self):
        """ Save the logged data to a CSV file. """
        d = {'tick': self.ticks, 'rewards': self.rewards, 'vels': self.velocities}
        df = pd.DataFrame(data=d)
        df.to_csv("data.csv")

    def step(self, action):
        """
        Execute a single step in the environment.

        Args:
            action: The action to apply.

        Returns:
            obs: The new observation.
            reward: The reward for the step.
            done: Whether the episode has finished.
            info: Additional information.
        """
        self._apply_action(action)
        self._action1 = action

        obs = self._extract_obs()
        reward = self._calc_reward()
        self._reward = reward

        done = self._calc_done()
        info = {}

        self.iters += 1
        self.global_tick += 1

        if self.is_training:
            self.log()

        print('Reward:', reward)

        return obs, reward, done, info

    def _apply_action(self, action):
        """ Apply the given action to the simulation world. """
        self.control = action.tolist()
        self._world.player.apply_control(self.control)

    def _extract_obs(self, debug=True):
        """ Extract observations from the simulation world. """
        Carsim_pos = self._world.player.get_location()
        Carsim_vel = self._world.player.get_velocity()
        Carsim_t = self._world.player.get_time()
        Carsim_r = self._world.player.get_yawrate()
        Carsim_rot = self._world.player.get_yaw()
        Carsim_done = self._world.player.get_done()

        pos_global = np.array([Carsim_pos[0], Carsim_pos[1]])
        vel_global = np.array([Carsim_vel[0], Carsim_vel[1]])
        yaw_global = radians(Carsim_rot)
        r = radians(Carsim_r)
        t_global = np.array(Carsim_t)

        s, l = pos_global
        v_y, v_x = vel_global
        yaw = yaw_global
        done = Carsim_done

        obs = np.array([s, l, v_x, v_y, yaw, r])

        norm_obs = np.array([-1 + 2 * (obs[i] - self._obs_min_vals[i]) / (self._obs_max_vals[i] - self._obs_min_vals[i]) for i in range(NUM_OBS)])

        self._velocity = np.linalg.norm(vel_global)
        self._s = s
        self._l = l
        self._vx = v_x
        self._vy = v_y
        self._yaw = yaw
        self._t = t_global
        self._done = done

        return norm_obs

    def _calc_reward(self):
        """ Calculate the reward for the current state. """
        pass  # Define your reward calculation logic here

    def _calc_done(self):
        """ Determine if the episode is complete. """
        return self._done

    def reset(self):
        """ Reset the environment for a new episode. """
        self.iters = 0
        self._world.reset_player()

        return self._extract_obs()

    def render(self, mode='none', close=False):
        """ Render the environment. """
        if mode == 'none':
            pass
        elif mode == 'gui':
            pass  # Implement GUI rendering if needed
