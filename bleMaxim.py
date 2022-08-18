import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from syncio import sync
from binascii import unhexlify, hexlify
from struct import *
import nest_asyncio
nest_asyncio.apply()

maxim_mac_addr = "00:18:80:9F:F8:B3"
uuid_rx = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"

commands = [
    "get_device_info\n",
    "set_cfg lcd time",
    "1653416056\n",
    "get_cfg sh_d hpar",
    "ams\n",
    "set_cfg sh_d hlpu",
    "blic 3058fa17316",
    "df922706fd834\n",
    "get_cfg sh_d hrpu",
    "blic\n",
    "get_cfg sh_auth\n",
    "set_cfg wearable",
    "suite scdenable",
    "1\n",
    "set_cfg blepower",
    "0\n",
    "set_cfg event_mo",
    "de 0\n",
    "set_cfg wearable",
    "suite algomode 2",
    "\n",
    "set_clg flash lo",
    "g 0\n",
    "set_cfg scdpower",
    "saving   1 10 5\n",
    "set_cfg stream b",
    "in\n",
    "read ppg 9\n"
]



def handle_rx(_: int, data: bytearray):
    global streamingData
    if data == b'\r\nread ppg 9 err=0\r\n':
        print("Recieved >>> ", data)
        streamingData = True
        print("Now streaming ppg data")
        return
    
    if not streamingData:
        print("Recieved >>> ", data)
    else:
        print("Recieved >>> ", data)

@sync
async def main(address):
    print("Connecting to device...")
    async with BleakClient(address) as client:
        global streamingData
        streamingData = False
        await client.start_notify(uuid_rx, handle_rx)
        print("Connected")

        for cmd in commands:
            await client.write_gatt_char(0x0024, unhexlify(cmd.encode('utf-8').hex()))
            print("Sent >>> ", unhexlify(cmd.encode('utf-8').hex()))
        
        while await client.is_connected():
            await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(maxim_mac_addr))