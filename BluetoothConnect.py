import asyncio
from bleak import BleakClient, BleakScanner
import time
import struct
from collections import namedtuple
import binascii
FsFileInfo = namedtuple('FsFileInfo', 'name size hash createDate')

async def device(mac):
    # scan for devices
    devices = await BleakScanner.discover()
    for d in devices:
        if d.address == mac:
            return d
    return None



def getNotified(sender, data):
    # name, size, hash, createDate = struct.unpack('<8sI4sQ', data)   
    # hash = '0x' + hash[::-1].hex()
    # fs_file_info = FsFileInfo(name=name, size=size, hash=hash, createDate=createDate)
    # print(sender, fs_file_info)
    file_path = "T13.hex"

    with open(file_path, "ab") as file:
        file.write(data)


def callBackForList(sender,data):
    # name, size, hash, createDate = struct.unpack('<8sI4sQ', data)   
    # hash = '0x' + hash[::-1].hex()
    # fs_file_info = FsFileInfo(name=name, size=size, hash=hash, createDate=createDate)
    # print(sender, fs_file_info)
    print(data)

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
                if key.split('-')[-1] == 'READ':
                    await client.start_notify(int(ref[key]), getNotified)
                         
            for key in ref:
                if key.split('-')[-1] == 'LIST':
                    await client.start_notify(int(ref[key]), callBackForList)

            
            # Write to the LIST characteristic first
            
            for key in ref:
                if key.split('-')[-1] == 'NUM':
                    numValue = await client.read_gatt_char(int(ref[key]))
            for key in ref:
                if key.split('-')[-1] == 'LIST':
                    
                    await client.write_gatt_char(int(ref[key]), numValue)

            for key in ref:
                if key.split('-')[-1] == 'READ':
                        await client.write_gatt_char(int(ref[key]), bytearray(b'T13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x27\x0F\x00\x00'))
            
            time.sleep(3)


            

asyncio.run(main())

