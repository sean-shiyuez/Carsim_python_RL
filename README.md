# Readme

---

# Carsim Python-MATLAB Integrated Simulation Environment

This project integrates Python and MATLAB to create a simulation environment for vehicle dynamics using Carsim and Simulink. It allows reinforcement learning algorithms to interact with Carsim simulations seamlessly.

## Features

- **Python-MATLAB Integration**: Utilizes MATLAB Engine for Python to communicate with Carsim simulations.
- **Reinforcement Learning (RL) Support**: Compatible with stable-baselines3 for RL algorithms like SAC.
- **Custom Environment**: Implements a custom Gym environment (`Drift_env`) for training vehicle control policies.
- **Simulink Interface**: Facilitates real-time simulation and control using MATLAB's Simulink.
- **High-Precision Dynamics**: Leverages Carsim's high-fidelity vehicle dynamics model for RL simulations.

---

## Requirements

### Python Dependencies

The required Python packages are listed in `requirements.txt`:

```
numpy==1.21.0
matplotlib==3.5.0
pandas==1.3.0
gym==0.21.0
stable-baselines3==1.6.0
```

### MATLAB Engine for Python

You must install MATLAB Engine for Python to enable communication with MATLAB. Refer to the **Installation Instructions** below.

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <https://github.com/your-repo/carsim-simulation.git>
cd carsim-simulation
```

### Step 2: Install Python Dependencies

Use pip to install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Install MATLAB Engine for Python

1. Navigate to the MATLAB installation directory:
    - **Windows**: `C:\\Program Files\\MATLAB\\R<version>\\extern\\engines\\python`
    - **macOS/Linux**: `/usr/local/MATLAB/R<version>/extern/engines/python`
2. Run the installation script:
    
    ```bash
    python setup.py install
    ```
    
3. Verify the installation:
    
    ```python
    import matlab.engine
    eng = matlab.engine.start_matlab()
    print("MATLAB Engine installed and connected successfully!")
    eng.quit()
    ```
    

---

## Usage

### Running the Simulation

1. Ensure Carsim and Simulink models are configured properly (e.g., `Carsimenv` is loaded).
2. Run the main Python script:
    
    ```bash
    python main.py
    ```
    

### Training RL Models

The script integrates `stable-baselines3` for training RL policies. Modify the parameters in `main.py` to customize the training setup (e.g., learning rate, batch size, etc.).

### Simulink Requirements

Ensure the Simulink model (`Carsimenv`) is correctly linked to the Carsim S-Function. Troubleshoot any missing paths or files in Simulink if errors occur.

---

## Known Issues

- **MATLAB-Python Interaction Speed**: The interaction speed between MATLAB and Python might be a bottleneck for real-time applications. Contributions to optimize this aspect are welcome.
- **Timestamp Alignment**: Ensure time synchronization between Python and Simulink when processing simulation results.

---

## File Structure

```
├── env.py              # Custom Gym environment
├── world.py            # Simulation environment setup
├── Carsim.py           # Carsim and MATLAB interaction
├── main.py             # Main script to run the simulation
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── Carsimenv.slx       # Simulink model file
```

---

## Example

A video demonstrating the simulation process is provided. Ensure to check the timestamp alignment between Carsim and Python outputs.

---

## Credits

While this project partially modifies the code from [auto-drift](https://github.com/angloth/auto-drift), its primary purpose differs:

- **Focus on High-Precision Dynamics**: This project emphasizes the use of Carsim's high-precision vehicle dynamics for reinforcement learning simulations, whereas `auto-drift` focuses more on drift control scenarios.
- **Integration with MATLAB and Simulink**: This project integrates MATLAB and Simulink, enabling advanced simulation and control capabilities not present in the original project.
- **Versatile RL Applications**: Beyond drift scenarios, this project supports broader applications in vehicle control and safety-critical scenarios.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

- [Carsim](https://www.carsim.com/) for providing advanced vehicle simulation.
- [MATLAB](https://www.mathworks.com/products/matlab.html) for its robust engineering tools.
- [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) for reinforcement learning support.
