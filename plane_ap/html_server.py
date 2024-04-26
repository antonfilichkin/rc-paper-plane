import asyncio
import aiofile


HTTP_HEADER = b'HTTP/1.0 200 OK\r\n'
CONTENT_TYPE = b'Content-type: text/html\r\n'


async def webpage_bytes():
    with aiofile.open('web_ui.html', 'r') as page:
        return page.read().encode('utf-8')



async def handle_client(reader, writer):
    print('Client connected.')
    request = await reader.read(1024)
    print(f"Request: '{request}'")

    writer.write(HTTP_HEADER)
    writer.write(CONTENT_TYPE)
    writer.write(b'\r\n')
    writer.write(webpage_bytes())
    writer.write(b'\r\n')
    await writer.drain()
    await writer.wait_closed()
    print('Client disconnected.')


async def run_server():
    await asyncio.start_server(handle_client, '0.0.0.0', 80)
