from machine import deepsleep
import asyncio
import wifi
import config
import common
import html_server


def power_off():
    print("Power OFF!")
    deepsleep()


def mayday():
    print('Alarm!')


connection_lost_sec = 0


async def connection_watchdog():
    global connection_lost_sec
    while True:
        if wifi.is_connected():
            await common.blink(2, 100)
        elif connection_lost_sec >= config.WIFI_LOST_POWER_OFF_SEC:
            power_off()
        else:
            mayday()
            connection_lost_sec += 1
        await asyncio.sleep(1)


# Initial connect
if not wifi.wait_for_connection(30, 5):
    power_off()

loop = asyncio.get_event_loop()
loop.set_exception_handler(common.exception_handler)
loop.create_task(connection_watchdog())
loop.create_task(html_server.run_server())
loop.run_forever()
