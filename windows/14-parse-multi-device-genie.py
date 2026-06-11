import json
import sys

from radkit_ntc import parse
from radkit_client import Client

if len(sys.argv) != 5:
    print(
        "Usage: python windows/14-parse-multi-device-genie.py "
        "<user_id> <service_id> <target_device_1> <target_device_2>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device_1 = sys.argv[3]
target_device_2 = sys.argv[4]

commands = [
    "show version",
    "show memory statistics",
]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_devices = service.inventory.filter("name", target_device_1)
    my_devices.add(target_device_2)

    multiple_response = my_devices.exec(commands).wait()
    parsed_response = parse(multiple_response)

    for device_name in [target_device_1, target_device_2]:
        print(f"\n📱 {device_name}")
        for command in commands:
            result = parsed_response[device_name][command]
            print(f"🧾 {command}")
            print(f"Status: {result.status}")
            print(f"{json.dumps(dict(result.data.items()), indent=2)}\n----------")
