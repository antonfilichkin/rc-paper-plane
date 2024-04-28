import asyncio
import aioespnow
import time
import json

e = aioespnow.AIOESPNow()
e.active(True)


def add_peer(peer: bytes):
    print(f"Adding new peer '{peer}'.")
    e.add_peer(peer)
    time.sleep(1)


def handle_error(err):
    if len(err.args) > 1:
        if err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
            print('Ignoring error: ESP_ERR_ESPNOW_NOT_FOUND')
            return
        if err.args[1] == 'ESP_ERR_ESPNOW_IF':
            print('Ignoring error: ESP_ERR_ESPNOW_IF')
            return
        if err.args[1] == 'ESP_ERR_ESPNOW_EXIST':
            print('Ignoring error: ESP_ERR_ESPNOW_EXIST')
            return
    raise err


async def send(peer: bytes, m_type: str, data):
    message = json.dumps({"type": m_type, "data": data})
    # print('message', message)
    try:
        # print(f"Sending: '{message}' to '{peer}'.")
        if not await e.asend(peer, message.encode('utf-8')):
            print(f"Peer '{peer}' not responding!")
        else:
            pass
            # print(f"Data sent: '{message}'.")
    except OSError as err:
        handle_error(err)


async def receive():
    while True:
        mac, msg = e.recv()
        if msg:
            data = msg.decode('utf-8')
            # print(f"Received: '{data}' from '{mac}'.")
            # await asyncio.sleep(1)
            yield data
