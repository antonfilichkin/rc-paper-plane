from machine import Pin, PWM
import asyncio
import server

IN1_PIN = 0
IN2_PIN = 1
IN3_PIN = 3
IN4_PIN = 4
POWER_PIN = 10

MAX_DUTY_CYCLE = 65535
MIN_DUTY_CYCLE = 0
FREQUENCY = 20000

__l_pwm__ = PWM(Pin(IN1_PIN, Pin.OUT))
__l_dir__ = PWM(Pin(IN2_PIN, Pin.OUT))
__r_pwm__ = PWM(Pin(IN3_PIN, Pin.OUT))
__r_dir__ = PWM(Pin(IN4_PIN, Pin.OUT))

__l_pwm__.freq(FREQUENCY)
__l_dir__.freq(FREQUENCY)
__r_pwm__.freq(FREQUENCY)
__r_dir__.freq(FREQUENCY)

__power__ = Pin(POWER_PIN, Pin.OUT)


def rate_to_u16(rate: int):
    return int(rate * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE) / 100)


def set_throttle(left: int, right: int, button_state: int):
    __l_pwm__.duty_u16(rate_to_u16(left))
    __r_pwm__.duty_u16(rate_to_u16(right))
    if button_state:
        __power__.on()
        print(f"Throttle: left '{left}', right '{right}'.")
    else:
        __power__.off()
        print(f"Throttle OFF.")


def power_off():
    set_throttle(0, 0, 0)
    print("Disabled DRV8833.")


def power_on():
    set_throttle(0, 0, 1)
    print("Enabled DRV8833.")


async def send():
    while True:
        await server.send(f'{{"type": "plane", "data": {{"motor": {__power__.value()}}}}}')
        await asyncio.sleep(10)

power_off()
