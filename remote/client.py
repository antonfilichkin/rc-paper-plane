import aioespnow

PLANE_PEER = b'd\xe83\x8d\x8c\x89'

e = aioespnow.AIOESPNow()
e.active(True)
e.add_peer(PLANE_PEER)


async def send(data):
    if not await e.asend(PLANE_PEER, data.encode('utf-8')):
        print(f"Plane not responding! (peer: '{PLANE_PEER}')")
    else:
        print(f"Data sent: '{data}'")


async def receive():
    async for mac, msg in e:
        print(f"Received: '{msg}'")

