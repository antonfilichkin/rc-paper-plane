import asyncio

import client
import joystick


async def print_data():
    while True:
        print(f"Print task: {joystick.read()}")
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.create_task(joystick.send())
loop.create_task(client.receive())
loop.run_forever()
