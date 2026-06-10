import sys

from radkit_client import Client, ExecStatus

if len(sys.argv) not in (4, 5):
    print(
        "Usage: python scripts/11-push-config-single-device.py "
        "<user_id> <service_id> <target_device> [loopback_id]"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device = sys.argv[3]
loopback_id = sys.argv[4] if len(sys.argv) == 5 else "802"

new_config = f"""configure terminal
interface Loopback{loopback_id}
description TestRADKit
end"""

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_device = service.inventory[target_device]
    exec_result = my_device.exec(new_config).wait()

    if exec_result.status == ExecStatus.SUCCESS:
        print(f"\n✅ Execution Status: {exec_result.status}\n")
        print(f"📦 Raw Data: {exec_result.raw_data}")
    else:
        print(f"❌ Command execution failed: {str(exec_result.errors)}")
