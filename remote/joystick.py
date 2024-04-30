from machine import ADC, Pin
import asyncio

X_MIN = 0
X_MID = 32767
X_MAX = 65535
Y_MAX = 0
Y_MIN = 32767

JOY_X_PIN = 4
JOY_Y_PIN = 3
JOY_BUTTON = 1
JOY_BUTTON_DEBOUNCE_DELAY_MS = 20

joy_x = ADC(JOY_X_PIN)
joy_x.atten(ADC.ATTN_11DB)

joy_y = ADC(JOY_Y_PIN)
joy_y.atten(ADC.ATTN_11DB)

joy_button = Pin(JOY_BUTTON, Pin.IN, Pin.PULL_UP)

button_state = False


def calibrate():
    global X_MID, Y_MIN
    ms_to_configure = 200
    read_interval_ms = 10

    x_mid_calculated = X_MID
    y_min_calculated = Y_MIN
    for _ in range(0, ms_to_configure, read_interval_ms):
        x_mid_calculated = (x_mid_calculated + joy_x.read_u16()) / 2
        y_min_calculated = (y_min_calculated + joy_y.read_u16()) / 2

    X_MID = int(x_mid_calculated)
    Y_MIN = int(y_min_calculated)
    print(f"Calibrated joystick! 'X_MID={X_MID}, Y_MIN={Y_MIN}'")


async def read_button():
    global button_state
    while True:
        current = joy_button.value()
        active = 0
        while active < JOY_BUTTON_DEBOUNCE_DELAY_MS:
            if current == joy_button.value():
                active += 1
            else:
                active = 0
                asyncio.sleep_ms(1)
        if active == JOY_BUTTON_DEBOUNCE_DELAY_MS:
            button_state = joy_button.value()
        await asyncio.sleep_ms(20)


def get_raw_data():
    x = joy_x.read_u16()
    y = joy_y.read_u16()
    return {'x': x, 'y': y, 'button': button_state}


def __thrust__():
    y = joy_y.read_u16()
    if y > Y_MIN:
        thrust = 0
    else:
        thrust = ((Y_MIN - y) / (Y_MIN - Y_MAX)) * 100
    if thrust < 0:
        return 0
    return int(thrust)


def __turn__():
    x = joy_x.read_u16()
    if x > X_MID:
        turn = (x - X_MID) / (X_MAX - X_MID) * 100
    else:
        turn = -(X_MID - x) / (X_MID - X_MIN) * 100
    return int(turn)


def to_motors_throttle():
    thrust = __thrust__()
    turn = __turn__()

    if turn < 0:
        l_throttle = int(thrust - thrust * (-turn / 100))
        r_throttle = thrust
    else:
        l_throttle = thrust
        r_throttle = int(thrust - thrust * (turn / 100))

    button = not bool(button_state)
    if button:
        return {'left': l_throttle, 'right': r_throttle, 'button': button}
    else:
        return {'left': l_throttle, 'right': r_throttle}