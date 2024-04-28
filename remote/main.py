from machine import deepsleep
import asyncio
import wifi
import config
import common
import joystick
import esp_now


plane_mac = b''


def power_off():
    print("Power OFF!")
    deepsleep()


def mayday():
    print('Alarm!')


def setup():
    if not wifi.connect(10, 2):
        power_off()

    joystick.calibrate()

    global plane_mac
    plane_mac = wifi.get_plane_mac()
    if not plane_mac:
        power_off()
    esp_now.add_peer(plane_mac)


async def connection_watchdog():
    connection_lost_sec = 0
    while True:
        if wifi.is_connected():
            await esp_now.send(plane_mac, 'ping', {"status": "OK"})
            await common.blink(2, 100)
        elif connection_lost_sec >= config.WIFI_LOST_POWER_OFF_SEC:
            power_off()
        elif not wifi.connect(5, 1):
            mayday()
            connection_lost_sec += 5
        await asyncio.sleep(0.5)


def __is_update_needed__(sent_data, new_data):
    change_threshold = 1

    if sent_data['button'] != new_data['button']:
        return True

    sent_throttle = sent_data['throttle']
    new_throttle = new_data['throttle']

    if abs(sent_throttle['left'] - new_throttle['left']) > change_threshold:
        return True

    if abs(sent_throttle['right'] - new_throttle['right']) > change_threshold:
        return True


async def send_command():
    command_send_interval_ms = 100
    old_data = joystick.to_motors_throttle()
    await esp_now.send(plane_mac, 'motor', old_data)
    while True:
        await asyncio.sleep_ms(command_send_interval_ms)
        new_data = joystick.to_motors_throttle()
        if __is_update_needed__(old_data, new_data):
            await esp_now.send(plane_mac, 'motor', new_data)
            old_data = new_data
        await asyncio.sleep(0.5)


setup()

loop = asyncio.get_event_loop()
loop.set_exception_handler(common.exception_handler)
loop.create_task(connection_watchdog())
loop.create_task(joystick.read_button())
loop.create_task(send_command())
loop.run_forever()
