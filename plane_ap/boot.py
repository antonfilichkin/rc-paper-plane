import esp
import gc
import network


esp.osdebug(None)
gc.collect()

SSID = 'Paper-plane-1'
PASSWORD = '12345678'

wlan = network.WLAN(network.AP_IF)
wlan.disconnect()
wlan.active(True)
wlan.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA_WPA2_PSK)

while not wlan.active():
    pass

print(f"Access point activated!")
print(f"IP: '{wlan.ifconfig()[0]}'")
mac = ':'.join(['{:02X}'.format(byte) for byte in wlan.config('mac')])
print(f"MAC: '{mac}' ({wlan.config('mac')})")
