import sys

from radkit_client import Client

if len(sys.argv) != 4:
    print("Usage: python scripts/8-filter-inventory-by-device-type.py <user_id> <service_id> <device_type>")
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
device_type = sys.argv[3]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()
    
    print("\n🔍 Filtered Inventory details:\n")

    for device in service.inventory.filter("device_type", device_type).values():
        print(f"📱  Device {device.name} is type {device.device_type}")
