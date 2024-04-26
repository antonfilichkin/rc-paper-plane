import asyncio
import aioespnow

e = aioespnow.AIOESPNow()
e.active(True)
peer = b'd\xe83\x83\x91\xb0'
e.add_peer(peer)


async def echo():
    async for mac, msg in e:
        print("Echo:", msg)
        try:
            await e.asend(mac, msg)
        except OSError as err:
            if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                e.add_peer(mac)
                await e.asend(mac, msg)


async def sleep():
    while True:
        print(f"Sleep")
        await asyncio.sleep(5)
