import sys

from radkit_client import Client

if len(sys.argv) != 4:
    print(
        "Usage: python scripts/12-single-device-multiple-commands.py "
        "<user_id> <service_id> <target_device>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device = sys.argv[3]

query_commands = ["show version | include Version|uptime", "show memory statistics"]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_device = service.inventory[target_device]
    exec_result_multiple = my_device.exec(query_commands).wait()

    print(f"\n📦 Output of command `show version | include Version|uptime` is: \n\n{exec_result_multiple['show version | include Version|uptime'].data}\n---------------\n")
    print(f"\n📦 Output of command `show memory statistics` is: \n\n{exec_result_multiple['show memory statistics'].data}\n---------------\n")
