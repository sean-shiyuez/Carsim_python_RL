function [s, l, vx, vy, yaw, r, t, done] = carenv(action, cmd)
    % Function to communicate with Simulink environment for Carsim simulation
    %
    % Args:
    %     action: Control action [steering, throttle] (cell array, converted to matrix)
    %     cmd: Command flag (0 for reset, 1 for step simulation)
    %
    % Returns:
    %     s: Longitudinal position
    %     l: Lateral position
    %     vx: Longitudinal velocity
    %     vy: Lateral velocity
    %     yaw: Yaw angle
    %     r: Yaw rate
    %     t: Simulation time
    %     done: Boolean indicating if the simulation is complete

    action = cell2mat(action);  % Convert cell array to matrix
    validate_action(action);    % Validate action inputs

    %% Reset simulation if cmd == 0
    if cmd == 0
        [clock, done_br] = reset_simulation();
    else
        [clock, done_br] = step_simulation(action);
    end

    % Extract simulation state variables
    px = clock(1);  % Longitudinal position
    py = clock(2);  % Lateral position
    vx = clock(3);  % Longitudinal velocity
    vy = clock(4);  % Lateral velocity
    yaw = clock(5);  % Yaw angle
    r = clock(6);  % Yaw rate
    t = clock(7);  % Simulation time

    % Convert Cartesian coordinates to longitudinal and lateral positions
    [s, l] = xy2sl(px, py);

    % Determine if the simulation is complete
    done = calculate_done(done_br, t, l, vx, vy);
end

function validate_action(action)
    % Validate action inputs to ensure they are within the expected range
    if any(action < -1) || any(action > 1)
        error('Action inputs must be between -1 and 1.');
    end
end

function [clock, done_br] = reset_simulation()
    % Reset the Simulink simulation environment
    global info;
    info = [0, 0, 0, 0, -1, 0, 0, 0];  % Initialize state info
    pause(5);  % Pause for stability

    try
        load_system('Carsimenv');  % Load Simulink system
        set_param('Carsimenv', 'SimulationCommand', 'stop');  % Stop simulation
        set_param('Carsimenv', 'SimulationCommand', 'start');  % Start simulation

        % Retry if the simulation does not start properly
        if info(end, 7) ~= 0.1
            pause(0.5);
            set_param('Carsimenv', 'SimulationCommand', 'start');
        end
        done_br = 0;
        clock = [0, 0, 0, 0, -1, 0, 0, 0];  % Reset state clock
    catch ME
        error('Failed to reset Simulink environment: %s', ME.message);
    end
end

function [clock, done_br] = step_simulation(action)
    % Step the Simulink simulation with the given action inputs
    t_be = evalin('caller', 'info(end, 7)');  % Retrieve previous simulation time
    set_param('Carsimenv/F_angle', 'Value', num2str(action(1)));  % Set steering input
    set_param('Carsimenv/Speedcontrol', 'Value', num2str(action(2)));  % Set throttle input
    set_param('Carsimenv', 'SimulationCommand', 'continue');  % Step simulation

    % Wait for simulation to advance
    t_now = evalin('caller', 'info(end, 7)');
    paus = 0;
    done_br = 0;

    while t_now == t_be
        t_now = evalin('caller', 'info(end, 7)');
        pause(0.1);
        paus = paus + 0.1;
        if paus >= 30
            % Stop simulation if it hangs
            set_param('Carsimenv', 'SimulationCommand', 'stop');
            done_br = 1;
            break;
        end
    end

    clock = evalin('caller', 'info(end, :)');  % Retrieve current state info
end

function done = calculate_done(done_br, t, l, vx, vy)
    % Determine if the simulation is complete
    MAX_TIME = 15;  % Maximum simulation time
    MAX_LATERAL_DEVIATION = 10;  % Maximum lateral deviation
    MIN_SPEED = 1;  % Minimum allowable speed

    if done_br == 1 || t >= MAX_TIME || abs(l) >= MAX_LATERAL_DEVIATION || sqrt(vx^2 + vy^2) <= MIN_SPEED
        done = 1;
    else
        done = 0;
    end
end
