"""
Spacecraft Intelligent Troubleshooting Test Bench

Version 0.1
Purpose:
    Simulate a spacecraft maintaining its orientation,
    generate sensor readings, inject faults, and collect
    data for automated testing and future AI diagnostics.
"""

import random
import matplotlib.pyplot as plt

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
        actual_angle_before = actual_angle
        sensor_reading = read_sensor(actual_angle_before, step)
        secondary_sensor_reading = read_secondary_sensor(actual_angle_before)
        temperature_reading = read_temperature_sensor(step)

        control_command = TARGET_ANGLE - sensor_reading
        actual_angle += control_command * 0.1  # Proportional control factor

        history.append({
            "step": step,
            "actual_angle": actual_angle_before,
            "next_actual_angle": actual_angle,
            "sensor_reading": sensor_reading,
            "secondary_sensor_reading": secondary_sensor_reading,
            "control_command": control_command,
            "temperature_reading": temperature_reading
        })

    return history


# ============================================================
# 3. SENSOR AND FAULT MODEL
# ============================================================

def read_sensor(actual_angle, step):
    """Generate a sensor reading, including noise and faults."""
    noise = random.uniform(-SENSOR_NOISE, SENSOR_NOISE)
    sensor_reading = actual_angle + noise

    if FAULT_START_STEP <= step < FAULT_START_STEP + 5:  # Fault lasts for 5 steps
        sensor_reading += FAULT_OFFSET

    return sensor_reading

def read_secondary_sensor(actual_angle):
    """Generate an independent secondary sensor reading."""
    noise = random.uniform(-SENSOR_NOISE, SENSOR_NOISE)
    return actual_angle + noise

def read_temperature_sensor(step):
    """Generate a temperature sensor reading, including noise and faults."""
    base_temperature = 70 + step * 0.5
    noise = random.uniform(-1.0, 1.0)
    temperature_reading = base_temperature + noise

    if step >= FAULT_START_STEP:
        temperature_reading += 20.0

    return temperature_reading


# ============================================================
# 4. AUTOMATED TESTING
# ============================================================

def run_tests(history):
    """Check whether the simulated spacecraft behaves correctly."""
    test_results = []

    for entry in history:
        step = entry["step"]
        actual_angle = entry["actual_angle"]
        primary_reading = entry["sensor_reading"]
        secondary_reading = entry["secondary_sensor_reading"]

        difference = abs(primary_reading - secondary_reading)
        MAX_DIFFERENCE = 5.0
        if difference > MAX_DIFFERENCE:
            test_results.append({
                "step": step,
                "error": "Primary and secondary sensor readings differ significantly"
            })

        if step > 0:
            previous_angle = history[step - 1]["actual_angle"]
            if abs(actual_angle - TARGET_ANGLE) > abs(previous_angle - TARGET_ANGLE):
                test_results.append({
                    "step": step,
                    "error": "Spacecraft moving away from target"
                })

    return test_results

def detect_rate_of_change_faults(history):
    """Flag unusually large changes in temperature readings."""
    detected_faults = []
    MAX_TEMPERATURE_CHANGE = 5.0

    for index in range(1, len(history)):
        previous = history[index - 1]["temperature_reading"]
        current = history[index]["temperature_reading"]
        change = current - previous

        if abs(change) > MAX_TEMPERATURE_CHANGE:
            detected_faults.append({
                "step": history[index]["step"],
                "change": change,
                "error": "Abnormal temperature rate of change"
            })

    return detected_faults


# ============================================================
# 5. RESULTS AND REPORTING
# ============================================================

def report_results(history, test_results):
    """Display a summary of the simulation and test results."""
    final_angle = history[-1]["next_actual_angle"]
    print(f"Final spacecraft angle: {final_angle:.2f} degrees")

    if not test_results:
        print("All angle tests passed successfully.")
    else:
        print(f"{len(test_results)} angle test(s) failed:")
        for result in test_results:
            print(f"  Step {result['step']}: {result['error']}")

    steps = [entry["step"] for entry in history]
    actual_angles = [entry["actual_angle"] for entry in history]
    sensor_readings = [entry["sensor_reading"] for entry in history]
    secondary_sensor_readings = [entry["secondary_sensor_reading"] for entry in history]
    temperature_readings = [entry["temperature_reading"] for entry in history]

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(steps, actual_angles, label="Actual Angle", marker='o')
    plt.plot(steps, sensor_readings, label="Primary Sensor Reading", linestyle='--', marker='x')
    plt.plot(steps, secondary_sensor_readings, label="Secondary Sensor Reading", linestyle='-.', marker='^')
    plt.axvline(x=FAULT_START_STEP, color='red', linestyle='--', label="Fault Start")
    plt.xlabel("Time Step")
    plt.ylabel("Angle (degrees)")
    plt.title("Spacecraft Angle and Sensor Readings Over Time")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(steps, temperature_readings, label="Temperature Reading", color='orange', marker='s')
    plt.axvline(x=FAULT_START_STEP, color='red', linestyle='--', label="Fault Start")
    plt.xlabel("Time Step")
    plt.ylabel("Temperature (°F)")
    plt.title("Temperature Sensor Readings Over Time")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
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

    detected_faults = detect_rate_of_change_faults(history)
    print("\nRate-of-change fault detections:")
    for fault in detected_faults:
        print(
            f"  Step {fault['step']}: {fault['error']} "
            f"(change: {fault['change']:.2f} °F)"
        )


if __name__ == "__main__":
    main()
