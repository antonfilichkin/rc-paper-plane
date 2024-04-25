from machine import Pin, PWM
from comand import MotorCommand

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


def set_throttle(command: MotorCommand):
    __l_pwm__.duty_u16(rate_to_u16(command.left_power))
    __r_pwm__.duty_u16(rate_to_u16(command.right_power))
    if command.enabled:
        __power__.on()
        print(f"Throttle: left '{command.left_power}', right '{command.right_power}'.")
    else:
        __power__.off()
        print(f"Throttle OFF.")


def power_off():
    set_throttle(MotorCommand(False))
    print("Disabled DRV8833.")


def power_on():
    set_throttle(MotorCommand(True, 0, 0))
    print("Enabled DRV8833.")


power_off()
