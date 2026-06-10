import sys

from radkit_client import Client

if len(sys.argv) != 5:
    print(
        "Usage: python scripts/9-combine-inventory-filters.py "
        "<user_id> <service_id> <device_type_1> <device_type_2>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
device_type_1 = sys.argv[3]
device_type_2 = sys.argv[4]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    devices = service.inventory.filter("device_type", device_type_1) | service.inventory.filter(
        "device_type", device_type_2
    )
    
    print("\n🔍 Filtered Inventory details:\n")
        
    for device in devices.values():
        print(f"📱  Device {device.name} is type {device.device_type}")
