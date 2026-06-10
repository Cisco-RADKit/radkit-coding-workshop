import sys

from radkit_client import Client, ExecStatus

if len(sys.argv) != 6:
    print(
        "Usage: python scripts/18-download-file-sftp-scp.py "
        "<user_id> <service_id> <target_device> <remote_file> <local_file>"
    )
    sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
target_device = sys.argv[3]
remote_file = sys.argv[4]
local_file = sys.argv[5]

with Client.create() as client:
    client.sso_login(user_id)
    service = client.service_cloud(service_id).wait()

    my_device = service.inventory[target_device]

    print(f"🔐 Enabling SCP server on {target_device}...")
    new_config = """configure terminal
ip scp server enable
end"""
    exec_result = my_device.exec(new_config).wait()

    if exec_result.status == ExecStatus.SUCCESS:
        print(f"\n✅ Execution Status: {exec_result.status}\n")
        print(f"📦 Raw Data: {exec_result.raw_data}")
    else:
        print(f"❌ Command execution failed: {str(exec_result.errors)}")

    print(f"\n📁 Backing up startup-config to {remote_file} ...\n")

    quiet_prompt_enabled = False
    try:
        my_device.exec("configure terminal\nfile prompt quiet\nend").wait()
        quiet_prompt_enabled = True
    except Exception as exc:
        print(f"Could not enable 'file prompt quiet' (continuing): {exc}")

    try:
        copy_output = my_device.exec(f"copy startup-config {remote_file}").wait().data
        print(f"📝 {copy_output}")

        print(f"🔎 Verifying the file exists with 'dir {remote_file}'...")
        print(f"📄 {my_device.exec(f'dir {remote_file}').wait().data}")

        transfer_ok = False
        transfer_errors = []

        for protocol in ("sftp", "scp"):
            try:
                if protocol == "sftp":
                    req = my_device.sftp_download_to_file(remote_path=remote_file, local_path=local_file)
                else:
                    req = my_device.scp_download_to_file(remote_path=remote_file, local_path=local_file)

                req.show_progress()
                req.wait_closed()

                print(
                    f"Download completed with {protocol.upper()} from '{remote_file}' to '{local_file}'"
                )
                transfer_ok = True
                break
            except Exception as exc:
                error_text = str(exc)
                transfer_errors.append((protocol, error_text))
                print(f"{protocol.upper()} failed for '{remote_file}': {error_text}")

        if not transfer_ok:
            hint_lines = []
            for protocol, error_text in transfer_errors:
                lowered = error_text.lower()
                if protocol == "scp" and "administratively disabled" in lowered:
                    hint_lines.append("- SCP appears disabled. Enable with 'ip scp server enable'.")
                if protocol == "sftp" and "0 bytes read on a total of 4 expected bytes" in lowered:
                    hint_lines.append("- SFTP handshake failed. Verify SFTP subsystem and access policy.")

            if not hint_lines:
                hint_lines.append("- Verify SSH reachability, AAA permissions, and protocol support.")

            hint_text = "\n".join(dict.fromkeys(hint_lines))
            all_errors = "\n".join([f"- {proto.upper()}: {msg}" for proto, msg in transfer_errors])

            raise RuntimeError(
                "Download failed with all protocol attempts.\n"
                f"Errors:\n{all_errors}\n"
                f"Suggested fixes:\n{hint_text}"
            )
    finally:
        if quiet_prompt_enabled:
            try:
                my_device.exec("configure terminal\nno file prompt quiet\nend").wait()
            except Exception as exc:
                print(f"⚠️ Could not restore prompt behavior ('no file prompt quiet'): {exc}")
