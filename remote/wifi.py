import network
import time
import config
import common

sta_if = network.WLAN(network.STA_IF)


def enable_sta_if():
    print(f"Connecting to plane AP '{config.SSID}' ...")
    sta_if.active(True)

    if sta_if.isconnected():
        print('Started connected!')
        sta_if.disconnect()
    else:
        print('Started disconnected!')

    time.sleep(1)


def connect(max_retries: int, pause_sec: int) -> bool:
    counter = 0
    while max_retries > counter:
        try:
            sta_if.connect(config.SSID, config.PASSWORD)
        except OSError as e:
            if e.args[0] == 'Wifi Internal Error':
                pass

        time.sleep_ms(10)

        if not sta_if.isconnected():
            print(f"Plane AP '{config.SSID}' was not found! Retrying in '{pause_sec}' seconds.")
            common.sleep_with_blink(pause_sec, 1000)
            counter += 1
            continue
        elif sta_if.ifconfig()[0] == '0.0.0.0':
            pass
        else:
            print(f"Connected to plane AP!")
            print(f"IP: '{sta_if.ifconfig()[0]}'")
            mac = ':'.join(['{:02X}'.format(byte) for byte in sta_if.config('mac')])
            print(f"MAC: '{mac}' ({sta_if.config('mac')})")
            return True

    print(f"Failed to connect to '{config.SSID}'. After '{max_retries}' retries.")
    time.sleep_ms(10)
    return False


def is_connected() -> bool:
    return sta_if.isconnected()
