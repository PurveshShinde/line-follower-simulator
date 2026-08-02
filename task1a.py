"""
===================================================
    eLSI Sprint 1 - Task 1A : PID Line Following
    (Enhanced version)
===================================================
"""
import time
from connector_task1a import CoppeliaClient

SENSOR_ORDER = ['left_corner', 'left', 'middle', 'right', 'right_corner']

# ------------------------------------------------------------------
# POLARITY DETECTION
# ------------------------------------------------------------------
# NOTE: this track has TWO zones with opposite color schemes (visible
# in the scene screenshot as a diagonal split) - one half is a white
# background with a black line, the other half is a black background
# with a white line. That means a single fixed "calibrate once at
# startup" polarity does NOT work here: the robot needs to re-detect
# polarity every frame as it crosses the boundary.
#
# The old code tried this with `sum(sensor_values) > 2.5`, which is
# fragile - it's just a magnitude threshold that misfires depending on
# how many sensors happen to be covered right now (e.g. at the
# diagonal boundary, on wide curves, or partial coverage).
#
# More robust approach: after normalizing to 0..1, count how many
# sensors are "high" (>0.5) vs "low". A line only ever covers 1-3 of
# the 5 sensors; the background always covers the rest - so whichever
# group is the MINORITY is the line, regardless of whether that
# minority reads high or low. This works the same way in both zones
# of the track without needing to know which color is "line" in
# advance.
# ------------------------------------------------------------------

# PID memory variables
previous_error = 0.0
integral = 0.0

# PID constants
Kp = 1.3
Ki = 0.0
Kd = 0.35
INTEGRAL_LIMIT = 5.0         # anti-windup clamp (only matters once Ki > 0)

BASE_SPEED = 2.4
MIN_SPEED = 0.2
MAX_SPEED = 4.0

# Position weights from left to right
WEIGHTS = [-2, -1, 0, 1, 2]

# Contrast threshold below which we say "no line visible"
CONTRAST_THRESHOLD = 0.15
LINE_LOST_THRESHOLD = 0.05

# Recovery turn speeds when the line is completely lost
LOST_SLOW = 0.8
LOST_FAST = 2.6


def control_loop(sensors):
    """
    Return left_speed and right_speed according to sensor values.
    """
    global previous_error
    global integral

    sensor_values = [sensors[k] for k in SENSOR_ORDER]

    # ----------------------------------------------------
    # Normalize, then detect polarity per-frame via minority vote.
    # ----------------------------------------------------
    min_val = min(sensor_values)
    max_val = max(sensor_values)
    contrast = max_val - min_val

    if contrast > CONTRAST_THRESHOLD:
        sensor_values = [(val - min_val) / contrast for val in sensor_values]

        # Minority-vote polarity detection: count sensors reading
        # "high" (>0.5) after normalization. A line only ever covers
        # 1-3 of 5 sensors, so whichever group (high or low) is
        # SMALLER is the line - regardless of which raw color that
        # corresponds to. This adapts correctly on both halves of the
        # track without needing to know in advance which side is which.
        high_count = sum(1 for v in sensor_values if v > 0.5)
        if high_count > 2:
            # High readings are the majority -> that's the background,
            # so invert to make the line (minority, currently low) read high.
            sensor_values = [1.0 - val for val in sensor_values]
    else:
        sensor_values = [0.0] * 5

    total_value = sum(sensor_values)

    # If line is lost, turn based on previous direction
    if total_value < LINE_LOST_THRESHOLD:
        if previous_error < 0:
            return LOST_SLOW, LOST_FAST
        else:
            return LOST_FAST, LOST_SLOW

    # Weighted average position of the line
    position = sum(v * w for v, w in zip(sensor_values, WEIGHTS)) / total_value

    # Error: 0 means robot is centered on line
    error = position

    derivative = error - previous_error

    # Only accumulate the integral term when it's actually being used,
    # and clamp it to prevent windup once Ki > 0.
    if Ki != 0.0:
        integral += error
        integral = max(-INTEGRAL_LIMIT, min(INTEGRAL_LIMIT, integral))
    else:
        integral = 0.0

    correction = (Kp * error) + (Ki * integral) + (Kd * derivative)
    previous_error = error

    left_speed = BASE_SPEED + correction
    right_speed = BASE_SPEED - correction

    left_speed = max(MIN_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(MIN_SPEED, min(MAX_SPEED, right_speed))

    return left_speed, right_speed


def main():
    client = CoppeliaClient(host="127.0.0.1", port=50002)
    client.connect()

    print("Connected to bridge_task1a. Running... (Ctrl+C to stop)")
    last_sensors = None
    try:
        while True:
            sensors = client.receive_sensor_data()
            if sensors is not None:
                last_sensors = sensors
            if last_sensors is None:
                time.sleep(0.02)
                continue
            left, right = control_loop(last_sensors)
            client.send_motor_command(left, right)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        try:
            client.send_motor_command(0.0, 0.0)
        except Exception:
            pass
        client.close()


if __name__ == "__main__":
    main()