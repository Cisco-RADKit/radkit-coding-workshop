import sys

from radkit_client import Client

if len(sys.argv) != 5:
    print(
        "Usage: python scripts/11-multi-device-single-command.py "
        "<user_id> <service_id> <target_device_1> <target_device_2>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device_1 = sys.argv[3]
target_device_2 = sys.argv[4]
query_command = "show version | include Version|uptime"

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_devices = service.inventory.filter("name", target_device_1)
    my_devices.add(target_device_2)
    
    print(my_devices)

    response = my_devices.exec(query_command).wait()

    for device_name, device_response in response.items():
        print(
            f"\n📱 Device {device_name} : "
            f"(Status is {device_response.status}) "
            f"Command '{device_response.command}' output is:\n"
            f"{device_response.data}\n----------\n"
        )
