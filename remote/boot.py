import esp
import gc
import network

esp.osdebug(None)
gc.collect()

SSID = 'Paper-plane-1'
PASSWORD = '12345678'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    pass

print(f"Access point activated!")
print(f"IP: '{wlan.ifconfig()[0]}'")
mac = ':'.join(['{:02X}'.format(byte) for byte in wlan.config('mac')])
print(f"MAC: '{mac}' ({wlan.config('mac')})")
