# ⚡ Execute Commands on Devices with RADKit and the Client API

One of the main features of the RADKit Client API is the interactivity with your inventory devices. You can retrieve, commit and parse configurations at will. Moreover, this API provides plenty of flexibility for optimising these operations across hundreds of devices at once - including filtering, one-to-many configs, many-to-many, and much more.  

## What you will learn
- Connect once and reuse the same client session across notebook cells
- Explore and filter inventory to select the right device targets
- Execute operational and configuration commands on one or many devices
- Parse raw CLI output with Genie for automation-friendly structured data
- Download files from devices with resilient SFTP/SCP fallback logic

---

To get started, open your console terminal and navigate to the directory `scripts/`.

---

## 1) Inspect and Filter Inventory

**Why this matters:** Before running automation, confirm which devices are available and choose precise targets.

**Workflow:**
1. Read devices from `service.inventory`.
2. Inspect key attributes such as `name`, `device_type`, and `host`.
3. Filter to a focused subset that matches your use case.

---

### 1.1 List Inventory Details

This example loops through all onboarded devices and prints basic identity fields.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 5-list-inventory-details.py your-remote-user-address your-service-id
```

After successfully authenticting in the browser window, the devices in the inventory of your own RADKit service will be displayed:

```bash
🔍 Inventory details:

📱 Device ftd-fdm is type FDM and has host 10.10.20.65
📱 Device c8000v is type IOS_XE and has host 10.10.20.21
📱 Device iosv-l2 is type IOS_XE and has host 10.10.20.22
📱 Device xrd is type IOS_XR and has host 10.10.20.27
📱 Device asav is type ASA and has host 10.10.20.23
```

> This is the Python code that you just ran:

<details>
<summary>Show 5-list-inventory-details.py</summary>

```python
# 5-list-inventory-details.py
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
```

</details>

---

### 1.2 Filter by Device Type

Use `inventory.filter()` to target only matching devices. This example filters the devices that match a specific platform type. We will filter the `IOS_XE` devices in our inventory.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 6-filter-inventory-by-device-type.py your-remote-user-address your-service-id IOS_XE
```

Only the `iosxe` devices shall appear:

```bash
🔍 Filtered Inventory details:

📱  Device c8000v is type IOS_XE
📱  Device iosv-l2 is type IOS_XE
```

> This is the Python code that you just ran:

<details>
<summary>Show 6-filter-inventory-by-device-type.py</summary>

```python
# 6-filter-inventory-by-device-type.py
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
```

</details>

---

### 1.3 Combine Multiple Filters

You can merge filtered inventories with `|` to build a broader target set. The next example combines `IOS_XR` and `IOS_XE` results into one `DeviceDict`.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 7-combine-inventory-filters.py your-remote-user-address your-service-id IOS_XR IOS_XE
```

Only the `iosxe` and `iosxr` devices will appear:

```bash
🔍 Filtered Inventory details:

📱  Device c8000v is type IOS_XE
📱  Device iosv-l2 is type IOS_XE
📱  Device xrd is type IOS_XR
```

> This is the Python code that you just ran:

<details>
<summary>Show 7-combine-inventory-filters.py</summary>

```python
# 7-combine-inventory-filters.py
import sys

from radkit_client import Client

if len(sys.argv) != 5:
  print(
    "Usage: python scripts/9-combine-inventory-filters.py "
    "<user_id> <service_id> <device_type_1> <device_type_2>"
  )
  sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]
device_type_1 = sys.argv[3]
device_type_2 = sys.argv[4]

with Client.create() as client:
  client.sso_login(user_id)
  service = client.service_cloud(service_id).wait()

  devices = service.inventory.filter("device_type", device_type_1) | service.inventory.filter(
    "device_type", device_type_2
  )

  print("\n🔍 Filtered Inventory details:\n")

  for device in devices.values():
    print(f"📱  Device {device.name} is type {device.device_type}")
```

</details>

---

## 2) Execute Commands on a Single Device

**Why this matters:** Single-device execution is the safest starting point for validation before wider rollouts.

**Workflow:**
1. Select one `Device` from `service.inventory`.
2. Call `exec()` with a show command or configuration payload.
3. Use `wait()` to get a `SingleExecResponse`.
4. Validate `status` and inspect `data`, `raw_data`, or `errors`.

---

### 2.1 Retrieve Operational Output

This example runs one show command on a target device and inspects the response fields, specifically `show ip interface brief` on device `iosv-l2`.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 8-exec-single-device-show.py your-remote-user-address your-service-id iosv-l2 "show ip interface brief"
```

Once the command execution is complete, you shall see the following details:

```bash
✅ Execution Status: ExecStatus.SUCCESS
📟 Device name: iosv-l2
🧬 Device type: IOS_XE
🧾 Device command: show ip interface brief
🆔 Client ID: asandovalros@gmail.com
☁️ Service ID: i0rf-v4tv-o6fd

📦 Raw Data: radkit-iosv#show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.10.20.22     YES TFTP   up                    up      
GigabitEthernet0/1     unassigned      YES unset  up                    up      
GigabitEthernet0/2     unassigned      YES unset  up                    up      
GigabitEthernet0/3     unassigned      YES unset  up                    up      
GigabitEthernet1/0     unassigned      YES unset  up                    up      
Vlan1                  unassigned      YES unset  administratively down down    
Vlan10                 unassigned      YES unset  administratively down down    
radkit-iosv#
```

> This is the Python code that you just ran:

<details>
<summary>Show 8-exec-single-device-show.py</summary>

```python
# 8-exec-single-device-show.py
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
```

</details>

---

### 2.2 Push Configuration Commands

`exec()` also supports configuration command strings, not only operational reads.

The next example pushes a loopback interface configuration and checks execution status. We provide the target device, as well as the id of the new loopback.

**Use caution in production environments:** validate on lab targets first and prefer idempotent config patterns where possible.


Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 9-push-config-single-device.py your-remote-user-address your-service-id iosv-l2 802
```

Once applied, we can see the details of the operation:

```bash
✅ Execution Status: ExecStatus.SUCCESS

📦 Raw Data: radkit-iosv#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
radkit-iosv(config)#interface Loopback802
radkit-iosv(config-if)#description TestRADKit
radkit-iosv(config-if)#end
radkit-iosv#
```

> This is the Python code that you just ran:

<details>
<summary>Show 9-push-config-single-device.py</summary>

```python
# 9-push-config-single-device.py
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
```

</details>

---

## 3) Execute Across Multiple Devices

**Why this matters:** Fan-out workflows let you run one automation step across many devices and aggregate outcomes quickly.

**Workflow:**
1. Build a `DeviceDict` using filters or manual additions.
2. Call `exec()` with one command or a list of commands.
3. Read results by device, by command, or both, depending on response shape.

---

### 3.1 Single Device, Multiple Commands

Pass a list of command strings to `exec()` when one device needs multiple checks in one request.

The response is `ExecResponse_ByCommand_ToSingle`, keyed by command text.

In this example, we will run the commands `show version | include Version|uptime` and `show memory statistics` in the target device `iosv-l2`, to then display the results.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 10-single-device-multiple-commands.py your-remote-user-address your-service-id iosv-l2
```

Once the commands are successfully executed, you shall see the following outputs:

```bash
📦 Output of command `show version | include Version|uptime` is: 

radkit-iosv#show version | include Version|uptime
Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Experimental Version 15.2(20200924:215240) [sweickge-sep24-2020-l2iol-release 135]
radkit-iosv uptime is 8 hours, 45 minutes
radkit-iosv#
---------------


📦 Output of command `show memory statistics` is: 

radkit-iosv#show memory statistics
                Head    Total(b)     Used(b)     Free(b)   Lowest(b)  Largest(b)
Processor    C2084A0   599981920    59527736   540454184   504464768   500969404
      I/O    79084A0    76546048    63588788    12957260    12920696    12746716
radkit-iosv#
---------------
```

> This is the Python code that you just ran:

<details>
<summary>Show 10-single-device-multiple-commands.py</summary>

```python
# 10-single-device-multiple-commands.py
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
```

</details>

---

### 3.2 Multiple Devices, Single Command

Run one command against a `DeviceDict` to compare results across devices.

The response type is `ExecResponse_ByDevice_ToSingle`, keyed by device name.

The following example runs the command `show version | include Version|uptime` in the two different devices provided.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 11-multi-device-single-command.py your-remote-user-address your-service-id iosv-l2 c8000v
```

After a bit, you will get the following outputs:

```bash
📱 Device c8000v : (Status is ExecStatus.SUCCESS) Command 'show version | include Version|uptime' output is:
radkit-cat8000v#show version | include Version|uptime
Cisco IOS XE Software, Version 17.15.01a
Cisco IOS Software [IOSXE], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.15.1a, RELEASE SOFTWARE (fc1)
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
GPL code under the terms of GPL Version 2.0.  For more details, see the
radkit-cat8000v uptime is 8 hours, 51 minutes
radkit-cat8000v#
----------


📱 Device iosv-l2 : (Status is ExecStatus.SUCCESS) Command 'show version | include Version|uptime' output is:
radkit-iosv#show version | include Version|uptime
Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Experimental Version 15.2(20200924:215240) [sweickge-sep24-2020-l2iol-release 135]
radkit-iosv uptime is 8 hours, 51 minutes
radkit-iosv#
----------
```

> This is the Python code that you just ran:

<details>
<summary>Show 11-multi-device-single-command.py</summary>

```python
# 11-multi-device-single-command.py
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
```

</details>

---

### 3.3 Multiple Devices, Multiple Commands

You can also pass a command list to a `DeviceDict` for full matrix execution.

The response becomes `ExecResponse_ByDevice_ByCommand`, a nested structure indexed by device, then command.

In this example, we will execute both the commands `show version | include Version|uptime` and `show processes cpu | include one minute` on the devices `iosv-l2` and `c8000v`.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 12-multi-device-multiple-commands.py your-remote-user-address your-service-id iosv-l2 c8000v
```

Once both commands are executed on both devices, you shall see the following output:

```bash
📱 iosv-l2
🧾 show version | include Version|uptime
Status: ExecStatus.SUCCESS
radkit-iosv#show version | include Version|uptime
Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Experimental Version 15.2(20200924:215240) [sweickge-sep24-2020-l2iol-release 135]
radkit-iosv uptime is 14 hours, 17 minutes
radkit-iosv#
----------
🧾 show processes cpu | include one minute
Status: ExecStatus.SUCCESS
radkit-iosv#show processes cpu | include one minute
CPU utilization for five seconds: 6%/0%; one minute: 0%; five minutes: 0%
radkit-iosv#
----------

📱 c8000v
🧾 show version | include Version|uptime
Status: ExecStatus.SUCCESS
radkit-cat8000v#show version | include Version|uptime
Cisco IOS XE Software, Version 17.15.01a
Cisco IOS Software [IOSXE], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.15.1a, RELEASE SOFTWARE (fc1)
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
GPL code under the terms of GPL Version 2.0.  For more details, see the
radkit-cat8000v uptime is 14 hours, 16 minutes
radkit-cat8000v#
----------
🧾 show processes cpu | include one minute
Status: ExecStatus.SUCCESS
radkit-cat8000v#show processes cpu | include one minute
CPU utilization for five seconds: 1%/0%; one minute: 0%; five minutes: 0%
radkit-cat8000v#
----------
```

> This is the Python code that you just ran:

<details>
<summary>Show 12-multi-device-multiple-commands.py</summary>

```python
# 12-multi-device-multiple-commands.py
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
```

</details>

---

## 4) Parse CLI Output with Genie

`radkit_genie` helps convert raw CLI text into structured data (`QDict`) so automation can access fields directly.

> Genie in RADKit supports more than parsing, but this lab focuses on parser-based workflows.

### Why parse raw CLI output?
Raw output is human-readable but difficult to process reliably in code. Parsed output removes most ad-hoc string matching and regex handling.

---

### 4.2 Setting radkit_genie

> ⚠️ The radkit_genie package must be installed separately and is currently not available in the Windows and macOS installers. You must use a pip based method to install it

> ⚠️ **If you are a Windows user**, navigate to the `windows/` folder of this repository and follow the steps below. The `uv` environment is different from the other OS types.

This repository includes the file `pyproject.toml` which installs all the RADKit libraries required to run this example.

If you have `uv` installed in your computer, navigate to the root of this repository and issue the following command:

```bash
uv sync
```

This will download all the required RADKit libraries and create the virtual environment `.venv` with all of them.

Now, to run the script you need to source this virtual environment based on the type of OS your computer is running (instructions here for [Windows](../setup/windows.md), [MacOS](../setup/macos.md) and [Linux](../setup/linux.md)).

### 4.1 Execute and Parse One Command

After collecting raw command output, call `parse_text()` with command and platform details.

Supported parser coverage is listed in the [Genie parser catalog](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers).

In this example, we will execute and parse the command `show version` on a `iosxe` device.

> Although not mandatory, it is possible to specify to the Genie parser the vendor type of the config being parsed. Genie will do a best-effort matching otherwise.

Execute the following command. Replace with your remote user address and service ID:

```bash
python 13-parse-single-command-genie.py your-remote-user-address your-service-id iosv-l2 "show version" iosxe
```

You should see the raw output, plus the parsed Python dictionary:

```bash
📋Raw command output:
radkit-iosv#show version
Cisco IOS Software, vios_l2 Software (vios_l2-ADVENTERPRISEK9-M), Experimental Version 15.2(20200924:215240) [sweickge-sep24-2020-l2iol-release 135]
Copyright (c) 1986-2020 by Cisco Systems, Inc.
Compiled Tue 29-Sep-20 11:53 by sweickge
 
 
ROM: Bootstrap program is IOSv
 
radkit-iosv uptime is 14 hours, 25 minutes
System returned to ROM by reload
System image file is "flash0:/vios_l2-adventerprisek9-m"
Last reload reason: Unknown reason
 
 
 
This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.
 
A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
 
If you require further assistance please contact us by sending email to
export@cisco.com.
 
Cisco IOSv () processor (revision 1.0) with 709857K/74752K bytes of memory.
Processor board ID 92MDDMVEC0G
2 Virtual Ethernet interfaces
5 Gigabit Ethernet interfaces
DRAM configuration is 72 bits wide with parity disabled.
256K bytes of non-volatile configuration memory.
0K bytes of ATA System CompactFlash 0 (Read/Write)
0K bytes of ATA CompactFlash 1 (Read/Write)
11264K bytes of ATA CompactFlash 2 (Read/Write)
0K bytes of ATA CompactFlash 3 (Read/Write)
 
Configuration register is 0x101
 
radkit-iosv#
--------------


🧞‍♂️Parsed command output (friendlier with your code):

{
  "version": {
    "version_short": "15.2",
    "platform": "vios_l2",
    "version": "15.2(20200924:215240)",
    "image_id": "vios_l2-ADVENTERPRISEK9-M",
    "label": "[sweickge-sep24-2020-l2iol-release 135]",
    "os": "IOS",
    "image_type": "developer image",
    "copyright_years": "1986-2020",
    "compiled_date": "Tue 29-Sep-20 11:53",
    "compiled_by": "sweickge",
    "rom": "Bootstrap program is IOSv",
    "hostname": "radkit-iosv",
    "uptime": "14 hours, 25 minutes",
    "returned_to_rom_by": "reload",
    "system_image": "flash0:/vios_l2-adventerprisek9-m",
    "last_reload_reason": "Unknown reason",
    "chassis": "IOSv",
    "main_mem": "709857",
    "processor_type": "",
    "rtr_type": "IOSv",
    "chassis_sn": "92MDDMVEC0G",
    "number_of_intfs": {
      "Virtual Ethernet": "2",
      "Gigabit Ethernet": "5"
    },
    "mem_size": {
      "non-volatile configuration": "256"
    },
    "processor_board_flash": "0K",
    "curr_config_register": "0x101"
  }
}
```

> This is the Python code that you just ran:

<details>
<summary>Show 13-parse-single-command-genie.py</summary>

```python
# 13-parse-single-command-genie.py
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
```

</details>

---

### 4.2 Parse Multiple Devices and Commands

**Why this matters:** Batch parsing keeps response handling consistent at scale.

**Workflow:**
1. Execute multiple commands on multiple devices.
2. Parse the combined response with `radkit_genie.parse()`.
3. Iterate by device and command to inspect `status` and structured `data`.

In this example, we will execute and parse on the same run the commands `show version` and `show memory statistics` on the devices `iosv-l2` and `c8000v`.

Execute the following command. Replace with your remote user address and service ID:

```bash
python 14-parse-multi-device-genie.py your-remote-user-address your-service-id iosv-l2 c8000v
```

You should see the raw and parsed versions of both commands on both devices:

```bash
📱 iosv-l2
🧾 show version
Status: ExecStatus.SUCCESS
{
  "version": {
    "version_short": "15.2",
    "platform": "vios_l2",
    "version": "15.2(20200924:215240)",
    "image_id": "vios_l2-ADVENTERPRISEK9-M",
    "label": "[sweickge-sep24-2020-l2iol-release 135]",
    "os": "IOS",
    "image_type": "developer image",
    "copyright_years": "1986-2020",
    "compiled_date": "Tue 29-Sep-20 11:53",
    "compiled_by": "sweickge",
    "rom": "Bootstrap program is IOSv",
    "hostname": "radkit-iosv",
    "uptime": "14 hours, 34 minutes",
    "returned_to_rom_by": "reload",
    "system_image": "flash0:/vios_l2-adventerprisek9-m",
    "last_reload_reason": "Unknown reason",
    "chassis": "IOSv",
    "main_mem": "709857",
    "processor_type": "",
    "rtr_type": "IOSv",
    "chassis_sn": "92MDDMVEC0G",
    "number_of_intfs": {
      "Virtual Ethernet": "2",
      "Gigabit Ethernet": "5"
    },
    "mem_size": {
      "non-volatile configuration": "256"
    },
    "processor_board_flash": "0K",
    "curr_config_register": "0x101"
  }
}
----------
🧾 show memory statistics
Status: ExecStatus.SUCCESS
{
  "name": {
    "processor": {
      "head": "C2084A0",
      "total": 599981920,
      "used": 59527768,
      "free": 540454152,
      "lowest": 504464768,
      "largest": 501001692
    },
    "i/o": {
      "head": "79084A0",
      "total": 76546048,
      "used": 63588788,
      "free": 12957260,
      "lowest": 12920696,
      "largest": 12746716
    }
  }
}
----------

📱 c8000v
🧾 show version
Status: ExecStatus.SUCCESS
{
  "version": {
    "xe_version": "17.15.01a",
    "version_short": "17.15",
    "platform": "Virtual XE",
    "version": "17.15.1a",
    "image_id": "X86_64_LINUX_IOSD-UNIVERSALK9-M",
    "label": "RELEASE SOFTWARE (fc1)",
    "os": "IOS-XE",
    "location": "IOSXE",
    "image_type": "production image",
    "copyright_years": "1986-2024",
    "compiled_date": "Wed 21-Aug-24 17:29",
    "compiled_by": "mcpre",
    "rom": "IOS-XE ROMMON",
    "hostname": "radkit-cat8000v",
    "uptime": "14 hours, 34 minutes",
    "uptime_this_cp": "14 hours, 35 minutes",
    "returned_to_rom_by": "reload",
    "system_image": "bootflash:packages.conf",
    "last_reload_reason": "factory-reset",
    "license_type": "Perpetual",
    "chassis": "C8000V",
    "main_mem": "1664235",
    "processor_type": "VXE",
    "rtr_type": "C8000V",
    "chassis_sn": "9QFQ2XHIPSJ",
    "router_operating_mode": "Autonomous",
    "number_of_intfs": {
      "Gigabit Ethernet": "4"
    },
    "mem_size": {
      "non-volatile configuration": "32768",
      "physical": "3960292"
    },
    "disks": {
      "bootflash:.": {
        "disk_size": "5234688",
        "type_of_disk": "virtual hard disk"
      }
    },
    "curr_config_register": "0x2102"
  }
}
----------
🧾 show memory statistics
Status: ExecStatus.SUCCESS
{
  "tracekey": "1#e738d74770d635700a4c4c39e0b09ed2",
  "name": {
    "processor": {
      "head": "7E39E2CF4048",
      "total": 1704038328,
      "used": 203243520,
      "free": 1500794808,
      "lowest": 1500743136,
      "largest": 1302355228
    },
    "reserve p": {
      "head": "7E39E2CF40A0",
      "total": 102404,
      "used": 92,
      "free": 102312,
      "lowest": 102312,
      "largest": 102312
    },
    "lsmpi_io": {
      "head": "7E39E0F561A8",
      "total": 3149400,
      "used": 3148576,
      "free": 824,
      "lowest": 824,
      "largest": 412
    }
  }
}
----------
```

> This is the Python code that you just ran:

<details>
<summary>Show 14-parse-multi-device-genie.py</summary>

```python
# 14-parse-multi-device-genie.py
import json
import sys

import radkit_genie
from radkit_client import Client

if len(sys.argv) != 5:
    print(
        "Usage: python scripts/16-parse-multi-device-genie.py "
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
    parsed_response = radkit_genie.parse(multiple_response)

    for device_name in [target_device_1, target_device_2]:
        print(f"\n📱 {device_name}")
        for command in commands:
            result = parsed_response[device_name][command]
            print(f"🧾 {command}")
            print(f"Status: {result.status}")
            print(f"{json.dumps(dict(result.data.items()), indent=2)}\n----------")
```

</details>

---

## 7) Handle Missing Parsers Safely

Not every command/platform combination has a built-in Genie parser. If parsing fails with `ParserNotFound`, verify support in the [official parser list](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers).

If no parser exists, you can build a custom parser and integrate it in RADKit workflows.

---

## 5) Download Files from Devices (`SFTP/SCP`)

**Why this matters:** File retrieval is a common automation need for backups, logs, and diagnostics.

**Workflow:**
1. Select the target device from inventory.
2. Prepare the file on the device (optional but common).
3. Attempt SFTP download first.
4. Automatically fallback to SCP if needed.
5. Wait for transfer completion and print actionable error hints if all attempts fail.

In this example, we will enable SCP on the device `iosv-l2`, generate the file of the startup configuration, and then download it to your computer. The remote file will be `flash:my-backup.cfg`, while the local file will be `my-backup.cfg` when saved.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 15-download-file-sftp-scp.py your-remote-user-address your-service-id flash:my-backup.cfg my-backup.cfg
```

You will see first how SCP is enabled in the device:

```bash
🔐 Enabling SCP server on iosv-l2...

✅ Execution Status: ExecStatus.SUCCESS

📦 Raw Data: radkit-iosv#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
radkit-iosv(config)#ip scp server enable
radkit-iosv(config)#end
radkit-iosv#
```

Afterwards, the startup config file will be generated and downloaded to your `scripts/` location:

```bash
📁 Backing up startup-config to flash:my-backup.cfg ...

📝 radkit-iosv#copy startup-config flash:my-backup.cfg
3233 bytes copied in 0.413 secs (7828 bytes/sec)
radkit-iosv#
🔎 Verifying the file exists with 'dir flash:my-backup.cfg'...
📄 radkit-iosv#dir flash:my-backup.cfg
Directory of flash0:/my-backup.cfg
 
  270  -rw-        3233  Jun 10 2026 00:23:42 +00:00  my-backup.cfg
 
2142715904 bytes total (2017718272 bytes free)
radkit-iosv#
SFTP failed for 'flash:my-backup.cfg': Performing action failed: 0 bytes read on a total of 4 expected bytes
00:25:09.360Z INFO  | Download complete [local_path='my-backup.cfg' bytes_read=3233]
my-backup.cfg 100.0% [==============================================================================>] 3233/3233 eta [00:00]
Download completed with SCP from 'flash:my-backup.cfg' to 'my-backup.cfg'
```

> This is the Python code that you just ran:

<details>
<summary>Show 15-download-file-sftp-scp.py</summary>

```python
# 15-download-file-sftp-scp.py
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
```

</details>

---

**This is it!** You have completed the RADKit Programmability 101 lab
