import sys

from radkit_client import Client, ExecStatus

if len(sys.argv) not in (4, 5):
    print(
        "Usage: python scripts/10-exec-single-device-show.py "
        "<user_id> <service_id> <target_device> [command]"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device = sys.argv[3]
command = sys.argv[4] if len(sys.argv) == 5 else "show ip interface brief"

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_device = service.inventory[target_device]
    exec_result = my_device.exec(command).wait()

    if exec_result.status == ExecStatus.SUCCESS:
        print(f"\n✅ Execution Status: {exec_result.status}")
        print(f"📟 Device name: {exec_result.device_name}")
        print(f"🧬 Device type: {exec_result.device_type}")
        print(f"🧾 Device command: {exec_result.command}")
        print(f"🆔 Client ID: {exec_result.client_id}")
        print(f"☁️ Service ID: {exec_result.service_id}\n")
        print(f"📦 Raw Data: {exec_result.raw_data}")
    else:
        print(f"Command execution failed: {exec_result.errors}")
