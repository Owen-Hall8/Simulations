
"""
Spacecraft Intelligent Troubleshooting Test Bench

Version 0.1
Purpose:
    Simulate a spacecraft maintaining its orientation,
    generate sensor readings, inject faults, and collect
    data for automated testing and future AI diagnostics.
"""

import random


# ============================================================
# 1. CONFIGURATION
# ============================================================

TARGET_ANGLE = 0.0       # Desired spacecraft orientation, degrees
INITIAL_ANGLE = 10.0     # Starting orientation, degrees
TIME_STEPS = 30          # Number of simulation steps
SENSOR_NOISE = 0.2       # Random sensor noise, degrees

FAULT_START_STEP = 15    # Step when a sensor fault begins
FAULT_OFFSET = 8.0       # Incorrect angle added by the fault


# ============================================================
# 2. SPACECRAFT SIMULATION
# ============================================================

def simulate_spacecraft():
    """Simulate spacecraft behavior over time."""

    actual_angle = INITIAL_ANGLE
    history = []

    for step in range(TIME_STEPS):
        # Generate a sensor reading from actual_angle.
        sensor_reading = read_sensor(actual_angle, step)

        # Calculate a control command that moves the spacecraft toward TARGET_ANGLE.
        control_command = TARGET_ANGLE - sensor_reading

        # Update actual_angle based on the control command and simulate the spacecraft's response.
        actual_angle += control_command * 0.1  # Assume a proportional control factor of 0.1

        # Save the step number, actual angle, sensor reading, and control command in history.
        history.append({
            "step": step,
            "actual_angle": actual_angle,
            "sensor_reading": sensor_reading,
            "control_command": control_command
        })

    return history


# ============================================================
# 3. SENSOR AND FAULT MODEL
# ============================================================

def read_sensor(actual_angle, step):
    """Generate a sensor reading, including noise and faults."""

    # Add random sensor noise.
    noise = random.uniform(-SENSOR_NOISE, SENSOR_NOISE)
    sensor_reading = actual_angle + noise

    # Apply FAULT_OFFSET when step >= FAULT_START_STEP.
    if step >= FAULT_START_STEP:
        sensor_reading += FAULT_OFFSET

    return sensor_reading


# ============================================================
# 4. AUTOMATED TESTING
# ============================================================

def run_tests(history):
    """Check whether the simulated spacecraft behaves correctly."""

    test_results = []

    for entry in history:
        step = entry["step"]
        actual_angle = entry["actual_angle"]
        sensor_reading = entry["sensor_reading"]
        control_command = entry["control_command"]

        # Check whether sensor readings are plausible.
        plausible = abs(sensor_reading - actual_angle) <= SENSOR_NOISE + FAULT_OFFSET
        if not plausible:
            test_results.append({"step": step, "error": "Implausible sensor reading"})

        # Detect when sensor readings disagree with reality.
        if step >= FAULT_START_STEP and abs(sensor_reading - actual_angle) < FAULT_OFFSET:
            test_results.append({"step": step, "error": "Fault not detected in sensor reading"})

        # Check whether the spacecraft approaches its target.
        if step > 0 and abs(actual_angle - TARGET_ANGLE) > abs(history[step - 1]["actual_angle"] - TARGET_ANGLE):
            test_results.append({"step": step, "error": "Spacecraft moving away from target"})

    return test_results


# ============================================================
# 5. RESULTS AND REPORTING
# ============================================================

def report_results(history, test_results):
    """Display a summary of the simulation and test results."""

    # Print the final spacecraft angle.
    final_angle = history[-1]["actual_angle"]
    print(f"Final spacecraft angle: {final_angle:.2f} degrees")

    # Summarize passed and failed tests.
    if not test_results:
        print("All tests passed successfully.")
    else:
        print(f"{len(test_results)} test(s) failed:")
        for result in test_results:
            print(f"  Step {result['step']}: {result['error']}")

    # Plot the spacecraft's actual angle and sensor readings over time.
    import matplotlib.pyplot as plt

    steps = [entry["step"] for entry in history]
    actual_angles = [entry["actual_angle"] for entry in history]
    sensor_readings = [entry["sensor_reading"] for entry in history]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, actual_angles, label="Actual Angle", marker='o')
    plt.plot(steps, sensor_readings, label="Sensor Reading", linestyle='--', marker='x')
    plt.axvline(x=FAULT_START_STEP, color='red', linestyle='--', label="Fault Start")
    plt.xlabel("Time Step")
    plt.ylabel("Angle (degrees)")
    plt.title("Spacecraft Angle and Sensor Readings Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


# ============================================================
# 6. MAIN PROGRAM
# ============================================================

def main():
    """Run the complete simulation and testing workflow."""

    print("Spacecraft Troubleshooting Test Bench")
    print("-------------------------------------")

    history = simulate_spacecraft()
    test_results = run_tests(history)
    report_results(history, test_results)


if __name__ == "__main__":
    main()
