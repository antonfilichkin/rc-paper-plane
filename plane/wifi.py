import network
import time
import config
import common

ap_if = network.WLAN(network.AP_IF)


def enable_ap_if():
    print(f"Starting plane AP '{config.SSID}' ...")
    ap_if.config(essid=config.SSID, password=config.PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)
    ap_if.active(True)

    time.sleep(1)

    print(f"Access point activated!")
    print("-------------------------")
    print(f"IP: '{ap_if.ifconfig()[0]}'")
    mac = ap_if.config('mac')
    print(f"MAC: '{common.mac_byte_to_str(mac)} ({mac})'")
    print("-------------------------")


def wait_for_connection(timeout_sec: int, pause_sec: int = 5) -> bool:
    counter = 0
    while True:
        if not is_connected():
            print(f"No connections found! New check in '{pause_sec}' seconds.")
            common.sleep_with_blink(pause_sec, 1000)
            counter += 1
            if counter * pause_sec > timeout_sec:
                print(f"No connections were found in {timeout_sec} seconds!")
                return False
            continue
        print("Connection established!")
        return True


def is_connected():
    return len(ap_if.status('stations')) > 0

