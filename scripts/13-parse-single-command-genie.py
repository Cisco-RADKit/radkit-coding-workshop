import json
import sys

import radkit_genie
from radkit_client import Client

if len(sys.argv) not in (4, 5, 6):
    print(
        "Usage: python scripts/15-parse-single-command-genie.py "
        "<user_id> <service_id> <target_device> [command] [platform_os]"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device = sys.argv[3]
query_command = sys.argv[4] if len(sys.argv) >= 5 else "show version"
platform_os = sys.argv[5] if len(sys.argv) == 6 else "iosxe"

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_device = service.inventory[target_device]
    exec_result_raw = my_device.exec(query_command).wait()
    print(f"\n📋Raw command output:\n{exec_result_raw.data}\n--------------\n")

    exec_result_parsed = radkit_genie.parse_text(exec_result_raw.data, query_command, os=platform_os)
    pretty_json = json.dumps(dict(exec_result_parsed), indent=2)
    print(f"\n🧞‍♂️Parsed command output (friendlier with your code):\n\n{pretty_json}\n")
