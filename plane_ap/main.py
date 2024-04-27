import asyncio
import server
import motors
import html_server

c = 0


async def sleep():
    global c
    while True:
        c += 1
        print(f"Sleep {c}")
        await asyncio.sleep(5)


def exception_handler(loop, context):
    exception = context['exception']
    message = context['message']
    print(f"Task failed, msg={message}, exception={exception}")


loop = asyncio.get_event_loop()
loop.set_exception_handler(exception_handler)
loop.create_task(server.receive())
# loop.create_task(motors.send())
loop.create_task(html_server.run_server())
loop.create_task(sleep())
loop.run_forever()

