import sys

from radkit_client import Client

if len(sys.argv) != 5:
    print(
        "Usage: python scripts/14-multi-device-multiple-commands.py "
        "<user_id> <service_id> <target_device_1> <target_device_2>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device_1 = sys.argv[3]
target_device_2 = sys.argv[4]

query_commands = [
    "show version | include Version|uptime",
    "show processes cpu | include one minute",
]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_devices = service.inventory.filter("name", target_device_1)
    my_devices.add(target_device_2)

    response = my_devices.exec(query_commands).wait()

    for device_name in [target_device_1, target_device_2]:
        print(f"\n📱 {device_name}")
        for command in query_commands:
            result = response[device_name][command]
            print(f"🧾 {command}")
            print(f"Status: {result.status}")
            print(f"{result.data}\n----------")
