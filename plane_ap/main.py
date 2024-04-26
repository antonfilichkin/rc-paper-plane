import asyncio
import server
import html_server


loop = asyncio.get_event_loop()
loop.create_task(server.echo())
loop.create_task(server.sleep())
loop.create_task(html_server.run_server())
loop.run_forever()
