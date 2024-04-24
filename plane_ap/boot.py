import esp
import gc
import network

esp.osdebug(None)
gc.collect()

ssid = 'Paper-plane-1'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

while not ap.active():
    pass

print(f"Access point activated! (IP: {ap.ifconfig()[0]})")
