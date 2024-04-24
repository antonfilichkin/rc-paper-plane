import joystick
from time import time, sleep

while True:
    x, y, button_state = joystick.read_joystick()

    # Print data with timestamp
    print(f"Time: {time():.2f} - Joystick X: {x}, Y: {y}, Button: {button_state}")

    # Sleep for 1 second
    sleep(1)
