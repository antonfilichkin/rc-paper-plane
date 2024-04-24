from machine import ADC, Pin


JOY_X_PIN = 4
JOY_Y_PIN = 3
JOY_BUTTON = 1


joy_x = ADC(JOY_X_PIN)
joy_x.atten(ADC.ATTN_11DB)

joy_y = ADC(JOY_Y_PIN)
joy_y.atten(ADC.ATTN_11DB)

joy_button = Pin(JOY_BUTTON, Pin.IN, Pin.PULL_UP)


def read_joystick():
    x_val = joy_x.read_u16()
    y_val = joy_y.read_u16()
    button_pressed = not joy_button.value()
    return x_val, y_val, button_pressed
