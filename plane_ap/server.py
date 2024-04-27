import asyncio
import aioespnow

e = aioespnow.AIOESPNow()
e.active(True)


def handle_error(mac, err):
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


async def receive():
    while True:
        async for mac, msg in e:
            try:
                print(e.peers_table)
                if mac not in e.peers_table.keys():
                    print("adding mac")
                    e.add_peer(mac)
                msg = msg.decode('utf-8')
                print(f"Received message from: '{mac}'")
                print(msg)
            except OSError as err:
                handle_error(mac, err)

#
# async def send(data):
#     while True:
#         peers = e.get_peers()
#         # print(f"Peers: {peers}")
#         if peers:
#             print(e.get_peers())
#             if not await e.asend(b'd\xe83\x83\x91\xb0', data):
#                 print(f"Peer not responding!")
#             else:
#                 print(f"Data sent: '{data}'")
#         else:
#             # print('No known peers!')
#             pass
