import numpy as np  # Import NumPy for numerical operations


# ==============================================================================
# -- Helper Functions ----------------------------------------------------------
# ==============================================================================

def get_actor_display_name(actor, truncate=250):
    """
    Get the display name of an actor.

    Args:
        actor: The actor object.
        truncate: Maximum length of the display name.

    Returns:
        str: Truncated display name of the actor.
    """
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name


# ==============================================================================
# -- Carsim World ---------------------------------------------------------------
# ==============================================================================

class world1:
    """
    Class representing the surrounding simulation environment.
    """

    def __init__(self, carsim_world):
        """
        Initialize the Carsim world.

        Args:
            carsim_world: The Carsim simulation world instance.
        """
        self.INI_CONTROL = np.array([0, 0, 0])  # Initial control values
        self.ini_a = self.INI_CONTROL.tolist()  # Convert initial control to list
        self.spawn_point = None  # Spawn point for the player (not used currently)
        self.world = carsim_world  # Reference to the Carsim world
        self.player = None  # Placeholder for the player object
        self.recording_enabled = False  # Flag for recording state
        self.recording_start = 0  # Starting point for recording
        self.name = 'SimulCarsim1'  # Name of the simulation environment

        # Initialize the environment
        self.restart()

    def reset_player(self):
        """
        Reset the player in the simulation.

        Stops the Simulink simulation and applies initial control to restart.
        """
        if self.player:
            self.player.run()  # Ensure the simulation is running
            self.player.apply_control(self.ini_a)  # Apply initial control

    def restart(self):
        """
        Restart the simulation environment.

        Spawns the player object and links it to the simulation world.
        """
        if self.player is not None:
            self.reset_player()

        # Ensure the player is initialized
        while self.player is None:
            # Attempt to link the player with the simulation world
            self.world.get_simulink(self)  # Get Simulink instance

            # Assign Carsim world to the player
            self.player = self.world()

# ==============================================================================
