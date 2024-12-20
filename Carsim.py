import matlab.engine  # Import MATLAB engine for Python-MATLAB integration
import numpy as np  # Import NumPy for numerical operations


class Carsim_world:
    """
    Class representing the Carsim simulation world integrated with MATLAB Simulink.
    """

    def __init__(self):
        """
        Initialize the Carsim simulation environment.
        """
        # Initial control values
        self.INI_CONTROL = np.array([0, 0, 0])
        self.a_ini = self.INI_CONTROL.tolist()

        # Flag indicating whether Simulink is running
        self.simulink = False

        # Start MATLAB engine
        self.eng = matlab.engine.start_matlab()
        self.simulink = True

        # Initialize simulation state variables
        self.px = 0  # Longitudinal position
        self.py = 0  # Lateral position
        self.vx = 60  # Longitudinal velocity
        self.vy = 0  # Lateral velocity
        self.t = 0  # Simulation time
        self.r = 0  # Yaw rate
        self.yaw = 0  # Yaw angle
        self.done = 0  # Simulation done flag
        self.control = []  # Last applied control inputs

    def run(self):
        """
        Stop the Simulink simulation.

        This method calls the Simulink model with the initial control values and a step flag set to 0.
        """
        self.eng.SimuCarsim(self.a_ini, 0, nargout=0)

    def get_simulink(self):
        """
        Load the necessary Simulink files and initialize the MATLAB engine.
        """
        self.eng = matlab.engine.start_matlab()
        self.eng.load('Shanghai_center.mat')  # Load the required data file

    def set_ini(self):
        """
        Reset the Simulink model to its initial state.

        This method stops the Simulink simulation by applying zero control inputs.
        """
        self.eng.SimuCarsim([0, 0, 0], 0, nargout=0)

    def apply_control(self, control):
        """
        Step the Simulink model with the specified control inputs.

        Args:
            control: A list of control inputs [steer, throttle, brake].
        """
        (self.s, self.l, self.vx, self.vy, self.yaw,
         self.r, self.t, self.done) = self.eng.SimuCarsim(control, 1, nargout=8)
        self.control = control

    def get_location(self):
        """
        Get the current position of the vehicle.

        Returns:
            tuple: Longitudinal and lateral positions (s, l).
        """
        return self.s, self.l

    def get_velocity(self):
        """
        Get the current velocity of the vehicle.

        Returns:
            tuple: Longitudinal and lateral velocities (vx, vy).
        """
        return self.vx, self.vy

    def get_time(self):
        """
        Get the current simulation time.

        Returns:
            float: Current simulation time.
        """
        return self.t

    def get_yaw(self):
        """
        Get the current yaw angle of the vehicle.

        Returns:
            float: Current yaw angle in radians.
        """
        return self.yaw

    def get_yawrate(self):
        """
        Get the current yaw rate of the vehicle.

        Returns:
            float: Current yaw rate in radians per second.
        """
        return self.r

    def get_control(self):
        """
        Get the last applied control inputs.

        Returns:
            list: The last applied control inputs.
        """
        return self.control

    def get_done(self):
        """
        Check if the simulation has reached a terminal state.

        Returns:
            bool: True if the simulation is done, False otherwise.
        """
        return self.done == 1

    def tick(self):
        """
        Placeholder method for future implementation of simulation ticking.
        """
        pass
