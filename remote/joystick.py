from machine import ADC, Pin
import asyncio
import client
import time

JOY_X_PIN = 4
JOY_Y_PIN = 3
JOY_BUTTON = 1
JOY_BUTTON_DEBOUNCE_DELAY = 50

joy_x = ADC(JOY_X_PIN)
joy_x.atten(ADC.ATTN_11DB)

joy_y = ADC(JOY_Y_PIN)
joy_y.atten(ADC.ATTN_11DB)

joy_button = Pin(JOY_BUTTON, Pin.IN, Pin.PULL_UP)

button_state = False


async def read_button():
    global button_state
    current = joy_button.value()
    active = 0
    while active < 20:
        if current == joy_button.value():
            active += 1
        else:
            active = 0
            time.sleep_ms(1)
    if active == 20:
        button_state = joy_button.value()
    await asyncio.sleep(0.1)


def read():
    x = joy_x.read_u16()
    y = joy_y.read_u16()
    return f'{{"type": "joystick", "data": {{"x": {x}, "y": {y}, "button": {button_state}}}}}'


async def send():
    while True:
        await read_button()
        await client.send(read())
        await asyncio.sleep(1)
