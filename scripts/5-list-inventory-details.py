import sys

from radkit_client import Client

if len(sys.argv) != 3:
    print("Usage: python scripts/7-list-inventory-details.py <user_id> <service_id>")
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()
    print("\n🔍 Inventory details:\n")

    for device in service.inventory.values():
        print(f"📱 Device {device.name} is type {device.device_type} and has host {device.host}")
