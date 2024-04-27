from machine import deepsleep
import asyncio
import wifi
import config
import common


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
        elif not wifi.connect(5, 1):
            mayday()
            connection_lost_sec += 5
        await asyncio.sleep(1)


# Initial connect
if not wifi.connect(6, 5):
    power_off()

loop = asyncio.get_event_loop()
loop.set_exception_handler(common.exception_handler)
loop.create_task(connection_watchdog())
# loop.create_task(send_motor())
# loop.create_task(client.receive())
loop.run_forever()

