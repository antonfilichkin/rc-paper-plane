from machine import Pin, PWM

IN1_PIN = 0
IN2_PIN = 1
IN3_PIN = 3
IN4_PIN = 4
POWER_PIN = 10

MAX_DUTY_CYCLE = 65535
MIN_DUTY_CYCLE = 0
FREQUENCY = 40000

__l_in_1__ = PWM(Pin(IN1_PIN, Pin.OUT))
__l_in_2__ = PWM(Pin(IN2_PIN, Pin.OUT))
__r_in_1__ = PWM(Pin(IN3_PIN, Pin.OUT))
__r_in_2__ = PWM(Pin(IN4_PIN, Pin.OUT))

__l_in_1__.freq(FREQUENCY)
__l_in_2__.freq(FREQUENCY)
__r_in_1__.freq(FREQUENCY)
__r_in_2__.freq(FREQUENCY)

__l_in_1__.duty_u16(MIN_DUTY_CYCLE)
__l_in_2__.duty_u16(MIN_DUTY_CYCLE)
__r_in_1__.duty_u16(MIN_DUTY_CYCLE)
__r_in_2__.duty_u16(MIN_DUTY_CYCLE)

__l_pmw__ = __l_in_1__
__r_pmw__ = __r_in_2__


# __power__ = Pin(POWER_PIN, Pin.OUT, value=1, hold=True) #1.23
__power__ = Pin(POWER_PIN, Pin.OUT, value=1)


__power_state__ = True


def rate_to_u16(rate: int):
    return int(rate / 100 * (MAX_DUTY_CYCLE - MIN_DUTY_CYCLE))


def power_off():
    set_throttle(MIN_DUTY_CYCLE, MIN_DUTY_CYCLE)
    __power__.off()
    print("Disabled DRV8833.")


def power_on():
    set_throttle(MIN_DUTY_CYCLE, MIN_DUTY_CYCLE)
    __power__.on()
    print("Enabled DRV8833.")


def set_throttle(left: int, right: int):
    print(f"Throttle: left '{left}', right '{right}'.")
    __l_in_1__.duty_u16(rate_to_u16(left))
    __r_in_1__.duty_u16(rate_to_u16(right))


def command(data):

    if data.get('button'):
        print("Power - invert.")
        __power__.value(not __power__.value())

    if __power__.value():
        set_throttle(data['left'], data['right'])


power_off()
