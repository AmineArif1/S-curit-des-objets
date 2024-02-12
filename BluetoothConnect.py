import asyncio
from bleak import BleakClient, BleakScanner
import time
import struct
async def device(mac):
    # scan for devices
    devices = await BleakScanner.discover()
    for d in devices:
        if d.address == mac:
            return d
    return None

byte_array = bytearray(b'T10\x00\x00\x00\x00\x00_\x08\x00\x00n\xe1\x0b\xfeH\x08er\xdc\x00\x00\x00')
hex_string = ''.join('{:02x}'.format(byte) for byte in byte_array)
print(hex_string)

def getNotified(sender,data):
    
    print(sender, data)

async def main():
    d = await device('DC:DC:FB:72:D4:56')
    async with BleakClient(d.address) as client:
        if client.is_connected:
            ref = {}
            numValue = 0
            print('connected')
            services = await client.get_services()
            for service in services:
                for charac in service.characteristics:
                    temp = str(str(charac) + " UNKNOWN").split()
                    ref[temp[0] + '-' + temp[3]] = temp[1:][1][:-2]
            
            # for key in ref:
            #     try:
            #          await client.start_notify(int(ref[key]), getNotified)
            #          print(key.split('-')[-1] + 'subbed')
            #     except:
                    
            #         pass
                    
            for key in ref:
                if key.split('-')[-1] == 'LIST':
                    await client.start_notify(int(ref[key]), getNotified)

            
            # Write to the LIST characteristic first
            
            for key in ref:
                if key.split('-')[-1] == 'NUM':
                    numValue = await client.read_gatt_char(int(ref[key]))
            for key in ref:
                if key.split('-')[-1] == 'LIST':
                    
                    await client.write_gatt_char(int(ref[key]), numValue)
            time.sleep(2)
            
           
            
asyncio.run(main())

