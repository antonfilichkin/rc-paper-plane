import time
from machine import deepsleep
import asyncio
import json
import wifi
import config
import common
import html_server
import esp_now
import motors


def power_off():
    print("Power OFF!")
    deepsleep()


def mayday():
    print('Alarm!')


async def connection_watchdog():
    connection_lost_sec = 0
    while True:
        if wifi.is_connected():
            await common.blink(2, 100)
        elif connection_lost_sec >= config.WIFI_LOST_POWER_OFF_SEC:
            power_off()
        else:
            mayday()
            connection_lost_sec += 1
        await asyncio.sleep(0.5)


async def execute_commands():
    while True:
        command = json.loads(next(esp_now.receive()))
        # print(f"Command: '{command}'.")
        if command['type'] == 'motor':
            motors.command(command['data'])
            await asyncio.sleep(0.1)


# Initial connect
if not wifi.wait_for_connection(30, 2):
    power_off()


loop = asyncio.get_event_loop()
loop.set_exception_handler(common.exception_handler)
loop.create_task(html_server.run_server())
loop.create_task(connection_watchdog())
loop.create_task(execute_commands())
loop.run_forever()
