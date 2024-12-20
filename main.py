from env import Drift_env  # Import the custom drift environment class
from World import world1  # Import the function to generate the world
from Carsim import Carsim_world  # Import the CarSim simulation world
from stable_baselines3 import SAC  # Import the SAC algorithm
from stable_baselines3.common.callbacks import CheckpointCallback  # Import the callback for saving model checkpoints

# Define the main function
def main():
    # Initialize the simulation world
    # world1 creates a world instance integrated with CarSim
    world = world1(Carsim_world)

    # Create the reinforcement learning environment
    # Drift_env is a custom environment that simulates 60 seconds with a 10ms step size
    env = Drift_env(world, simulation_time=60, step_time=10)

    # Initialize the reinforcement learning model
    # SAC uses a multilayer perceptron policy ("MlpPolicy") with specified parameters
    model = SAC(
        "MlpPolicy",  # Type of policy
        env,  # The associated environment
        verbose=0,  # Log output level, 0 means no output
        device="auto",  # Automatically choose GPU or CPU
        learning_rate=1e-5,  # Learning rate
        tensorboard_log="./SAC_tensorboard/",  # Path to save TensorBoard logs
        batch_size=256  # Batch size for training
    )

    # Create a callback for saving model checkpoints
    # Save the model every 5000 timesteps
    checkpoint_callback = CheckpointCallback(
        save_freq=5000,  # Frequency of saving
        save_path='./models/',  # Path to save models
        name_prefix='rl_model'  # Prefix for model filenames
    )

    # Start training the model
    model.learn(
        total_timesteps=int(1e5),  # Total training timesteps
        callback=checkpoint_callback,  # Callback function
        reset_num_timesteps=False,  # Do not reset the timestep counter
        tb_log_name="1124_run"  # Name for TensorBoard logs
    )

    # Save the final trained model
    model.save("Vehicle_Drift_test_1")

    # Save training logs
    env.save_logs()

    # Set the training flag to False
    env.is_training = False

    # Reset the environment for testing
    obs = env.reset()  # Reset the drift environment, restarting the world

    # Test the trained model
    while True:
        action, _states = model.predict(obs, deterministic=False)  # Predict actions using the model
        obs, rewards, done, info = env.step(action)  # Take action and get new state
        env.render()  # Render the environment
        if done:  # Check if the episode is finished
            obs = env.reset()  # Reset the environment after completion
            break

# Ensure the script executes the main function only when run directly
if __name__ == "__main__":
    main()
