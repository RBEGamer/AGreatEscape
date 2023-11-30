import asyncio
from bleak import BleakClient, BleakScanner
import asyncio
from bleak import BleakScanner
import random
import time
import math
import requests

def calculate_distance(txpower, rssi):
        ratio =(txpower-int(rssi))/40
        distance= math.pow(10,ratio)
        return distance


POS_X: int = 140
POS_Y: int = 178
M_PER_PIXEL:float = 30


async def main():
    devices = await BleakScanner.discover(timeout=1)
    for d in devices:
        try:
            print(d.address, calculate_distance(-40, d.rssi))
            pixels = calculate_distance(-40, d.rssi) * M_PER_PIXEL

            print(pixels)
            x = POS_X
            y = POS_Y
            for i in range(int(pixels)):
                op: int = random.randint(0,3)
                if op == 0:
                    x = x + 1 
                elif op == 1:
                    y = y + 1 
                elif op == 2:
                    x = x - 1 
                elif op == 3:
                    y = y - 1 

                
            
            requests.get("http://127.0.0.1:5557/api/setuserpos/{}/{}/{}".format(str(d.address),x,y))

            time.sleep(0.2)
            
        except:
            pass


while True:
    time.sleep(4)
    asyncio.run(main())

