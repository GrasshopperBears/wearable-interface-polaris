import asyncio
from time import sleep, time # 비동기화 모듈
from bleak import BleakClient

# 00001800-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Access Profile
#         uuid: 00001800-0000-1000-8000-00805f9b34fb
#         characteristic list:
#                  00002a00-0000-1000-8000-00805f9b34fb (Handle: 2):
#                 uuid: 00002a00-0000-1000-8000-00805f9b34fb
#                 description :
#                 properties : ['read', 'write']
# 00001801-0000-1000-8000-00805f9b34fb (Handle: 4): Generic Attribute Profile 
#         uuid: 00001801-0000-1000-8000-00805f9b34fb
#         characteristic list:
#                  00002a05-0000-1000-8000-00805f9b34fb (Handle: 5):
#                 uuid: 00002a05-0000-1000-8000-00805f9b34fb
#                 description :
#                 properties : ['read', 'indicate']
# 00001910-0000-1000-8000-00805f9b34fb (Handle: 8): Vendor specific
#         uuid: 00001910-0000-1000-8000-00805f9b34fb
#         characteristic list:
#                  00002b11-0000-1000-8000-00805f9b34fb (Handle: 9):
#                 uuid: 00002b11-0000-1000-8000-00805f9b34fb
#                 description :
#                 properties : ['write-without-response']
#                  00002b10-0000-1000-8000-00805f9b34fb (Handle: 11):
#                 uuid: 00002b10-0000-1000-8000-00805f9b34fb
#                 description :
#                 properties : ['notify']

address = "DC:23:4D:BB:89:D7"

# async def run(address):    
#     async with BleakClient(address) as client:
#         print('connected')
#         services = await client.get_services()        
#         for service in services:
#             print(service)             
#             # 서비스의 UUID 출력   
#             print('\tuuid:', service.uuid)
#             print('\tcharacteristic list:')
#             # 서비스의 모든 캐릭터리스틱 출력용
#             for characteristic in service.characteristics:
#                 # 캐릭터리스틱 클래스 변수 전체 출력
#                 print('\t\t', characteristic)
#                 # UUID 
#                 print('\t\tuuid:', characteristic.uuid)
#                 # decription(캐릭터리스틱 설명)
#                 print('\t\tdescription :', characteristic.description)
#                 # 캐릭터리스틱의 속성 출력
#                 # 속성 값 : ['write-without-response', 'write', 'read', 'notify']
#                 print('\t\tproperties :', characteristic.properties)

#     print('disconnect')

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run(address))
# print('done')



read_write_charcteristic_uuid = "00002b11-0000-1000-8000-00805f9b34fb"


async def after_notify():
    async with BleakClient("DC:23:4D:BB:89:D7") as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == read_write_charcteristic_uuid:
                    await client.write_gatt_char(characteristic, bytearray.fromhex('0051200511a3351013195921afe8420983de9081'))
                    await client.write_gatt_char(characteristic, bytearray.fromhex('016ca3780fdb11913a5b6f47ce7594788d26190f'))
                    await client.write_gatt_char(characteristic, bytearray.fromhex('024f0c90008ff5feb8bb6891a34ce929f078e6df'))
                    await client.write_gatt_char(characteristic, bytearray.fromhex('0399312e12fd57256845f544778243cf15d78cf4'))
                    await client.write_gatt_char(characteristic, bytearray.fromhex('04af8b9975c7543e'))
                    print("cb")


async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == '00002b10-0000-1000-8000-00805f9b34fb':
                    await client.start_notify(characteristic, after_notify)
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == read_write_charcteristic_uuid:
                    await client.write_gatt_char(characteristic, bytearray.fromhex('00212004d2f929e9cef1a849a601d3e20f5e1700'))
                    await client.write_gatt_char(characteristic, bytearray.fromhex('0163261caf6f36b13794eedfe5be8e7336'))
                    await asyncio.sleep(0.15)
                
                    print("data sent")

    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')
