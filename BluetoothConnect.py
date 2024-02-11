import asyncio
from bleak import BleakClient, BleakScanner

async def device(mac):
    # scan for devices
    devices = await BleakScanner.discover()
    for d in devices:
        if d.address == mac:
            return d
    return None

def getNotified(sender,data):
    print('here is your data sir')
    print(sender, data)

async def main():
    d = await device('D1:6A:16:01:A2:EC')
    async with BleakClient(d.address) as client:
        if client.is_connected:
            ref = {}
            print('connected')
            services = await client.get_services()
            for service in services:
                for charac in service.characteristics:
                    temp = str(str(charac) + " UNKNOWN").split()
                    ref[temp[0] + '-' + temp[3]] = temp[1:][1][:-2]
            
            print(ref)
            
            # Write to the LIST characteristic first
            # for key in ref:
            #     if key.split('-')[-1] == 'LIST':
       
            #         await client.write_gatt_char(int(ref[key]), bytearray(b'\x17\x00'))
            for key in ref:
                if key.split('-')[-1] == 'LIST':
                    await client.write_gatt_char(int(ref[key]), bytearray(b'\x17\x00'))
            for key in ref:
                if key.split('-')[-1] == 'LOG':
       
                    await  client.write_gatt_char(int(ref[key]), bytearray(b'\x02\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
            # Then start notifications
            for key in ref:
                if key.split('-')[-1] == 'ACK':
                   
                    await client.start_notify(int(ref[key]), getNotified)
            
            

            for key in ref:
                if key.split('-')[-1] == 'NUM':
                    await client.read_gatt_char(int(ref[key]))
            for key in ref:
                if key.split('-')[-1] == 'LOG':
              
                    print(await client.read_gatt_char(int(ref[key])))
            
            
asyncio.run(main())

