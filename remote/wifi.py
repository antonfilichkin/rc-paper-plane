import network
import time
import config
import common

sta_if = network.WLAN(network.STA_IF)
mac = str()
plane_mac = str()


def get_plane_mac() -> None or str:
    retries = 100
    sleep_time_sec = 0.5

    print('Getting plane MAC ', end='')
    while retries > 0:
        scan_results = sta_if.scan()
        if not scan_results:
            retries -= 1
            time.sleep(sleep_time_sec)
            print('.', end='')
            continue
        for ssid, bssid, channel, RSSI, authmode, hidden in scan_results:
            if ssid.decode('utf-8') == config.SSID:
                print(f"\nPlane MAC: '{common.mac_byte_to_str(plane_mac)} ({plane_mac})'")
                return bssid

    print(f"Failed to retrieve Plane MAC! After '{retries}' retries.")
    return None


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
    global mac, plane_mac
    counter = 0
    while max_retries > counter:
        try:
            sta_if.connect(config.SSID, config.PASSWORD)
        except OSError as e:
            if e.args[0] == 'Wifi Internal Error':
                pass

        time.sleep_ms(10)

        if not is_connected():
            print(f"Plane AP '{config.SSID}' was not found! Retrying in '{pause_sec}' seconds.")
            common.sleep_with_blink(pause_sec, 1000)
            counter += 1
            continue
        elif sta_if.ifconfig()[0] == '0.0.0.0':
            pass
        else:
            print(f"Connected to plane AP!")
            print("-------------------------")
            print(f"IP: '{sta_if.ifconfig()[0]}'")
            mac = sta_if.config('mac')
            print(f"MAC: '{common.mac_byte_to_str(mac)} ({mac})'")
            print("-------------------------")
            return True

    print(f"Failed to connect to '{config.SSID}'. After '{max_retries}' retries.")
    time.sleep_ms(10)
    return False


def is_connected() -> bool:
    return sta_if.isconnected()
