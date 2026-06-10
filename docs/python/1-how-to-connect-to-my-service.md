# 🔌 Connect to Your RADKit Service

There are many different ways to connect to your RADKit service. Depending on your environment, you will choose one over another.

## What you will do
- Connect through Cisco Cloud with SSO (most common)
- Connect with certificate-based login (automation friendly)
- Connect directly to your server without cloud access

---

To get started, open your console terminal, navigate to the directory `scripts/`, and input the following command:

```bash
radkit-client
```

This will open the `RADKit Client CLI` in your terminal window at the scripts directory of this repository.

## 1) Connect via Cisco Cloud (`SSO Login`)

**Best for**: Interactive use, development environments, and any scenario where a browser window can be opened.

**How it works**:

1. `sso_login` opens your web browser with the Cisco SSO login form.
2. The script pauses and waits until you complete the login.
3. Once authenticated, execution resumes automatically.

Execute the following command. Replace with your remote user address and service ID:

```bash
radkit-client script 1-authentication-sso.py your-remote-user-address your-service-id
```

You should be prompted to login in a new browser window. Once done, return to the CLI. The following messages should be displayed:

```bash
✅ Authentication successful!
✅ Connection successful to service i0rf-v4tv-o6fd!
```

> This is the Python code that you just ran:

<details>
<summary>Show Python code</summary>

```python
# 1-authentication-sso.py
import sys

from radkit_client import Client
from radkit_client.sync import ClientStatus, ServiceStatus # Nice enums to get the status of the client and service

if len(sys.argv) != 3:
	print("Usage: python scripts/1-authentication-sso.py <user_id> <service_id>")
	sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]

with Client.create() as client:
	client.sso_login(user_id)
	print("✅ Authentication successful!") if client.status == ClientStatus.CONNECTED else print("🔥 Connection failed ...")
    
	service = client.service_cloud(service_id).wait()
	print(f"✅ Connection successful to service {service.service_id}!") if service.status == ServiceStatus.READY else print(f"🔥 Connection to service {service.service_id} failed ...")
```

</details>

---

## 2) Certificate Login (`certificate_login`)

**Best for:** Non-interactive workflows such as CI/CD, scheduled jobs, or headless scripts.

**Why choose this:** No browser prompt is required during login. Authentication uses locally stored client certificates.

---
Before using this kind of login, you need to first generate the required security certificates for this user. To do that, you can use Python scripting.

Run the following command in your RADKit Client CLI. Replace with your remote user address:

```bash
radkit-client script 2-enroll-client.py your-remote-user-address
```

> This is the Python code that you just ran:

<details>
<summary>Show Python code</summary>

```python
# 2-enroll-client.py
import sys
from radkit_client import Client
from radkit_client.sync import ClientStatus

if len(sys.argv) != 2:
	print("Usage: python scripts/2-enroll-client.py <user_id>")
	sys.exit(1)

user_id = sys.argv[1]

with Client.create() as client:
	client.sso_login(user_id)
	if client.status == ClientStatus.CONNECTED:
		client.enroll_client() # Enroll the client to non-interactive cloud authentication (blocking call)
```

</details>

You will be prompted to login in a new browser window. Once done, return to the CLI, where you will be asked to provide a password.

Provide one, and remember it well! We will need it later.

After enrollment completes, run the next command in your CLI. Replace with your remote user address and service ID:

```bash
radkit-client script 3-certificate-login.py your-remote-user-address your-service-id
```

You will be prompted to provide your private key password, which is the one that we just created earlier:

```bash
🔑 Enter the password for your private key:
```

Once authenticated, you shall see the following messages without having to use the browser login anymore:

```bash
✅ Authentication successful!
✅ Connection successful to service i0rf-v4tv-o6fd!
```

> This is the Python code that you just ran:

<details>
<summary>Show Python code</summary>

```python
# 3-certificate-login.py
from radkit_client import Client
from radkit_client.sync import ClientStatus, ServiceStatus
import getpass
import sys

if len(sys.argv) != 3:
	print("Usage: python scripts/3-certificate-login.py <user_id> <service_id>")
	sys.exit(1)

user_id = sys.argv[1]
service_id = sys.argv[2]

private_key_password = getpass.getpass("🔑 Enter the password for your private key: ")

with Client.create() as client:
	client.certificate_login(identity=user_id, private_key_password=private_key_password)
	print("\n✅ Authentication successful!\n") if client.status == ClientStatus.CONNECTED else print("🔥 Connection failed ...")
    
	service = client.service_cloud(service_id).wait()
	print(f"\n✅ Connection successful to service {service.service_id}!\n") if service.status == ServiceStatus.READY else print(f"🔥 Connection to service {service.service_id} failed ...")
```

</details>

---

## 3) Connect Directly (`No Cloud`)

> ⚠️ If you don't have your VPN client installed, skip this part

**Best for:** Air-gapped environments, restricted outbound internet, or private-network-only deployments.

**Why choose this:** The client connects directly to the RADKit server endpoint over LAN/VPN, bypassing Cisco Cloud.

**You will need:**
- Your **CCO user ID**
- Your **E2EE validation token** (used as the password for direct auth)
- The server **hostname or IP address**
- The server **RPC port** (default: `8181`)

---

You need to connect first to your VPN using the Cisco Anyconnect VPN client and the following information:

- `Domain`: Domain that you received via e-mail
- `Username`: The VPN username you received via e-mail
- `Password`: The VPN password you received via e-mail

Once connected, execute the following command in the RADKit Client CLI. Replace with your remote user address:

```bash
radkit-client script 4-direct-login.py your-remote-user-address 
```

Provide your remote user's E2EE password when requested:

```bash
🔑 Enter your E2EE validation token:
```

Once done, you shall be prompted with the following confirmation. No need to use SSO login nor certificates, as this time it is the RADKit service which directly authenticated your request:

```bash
✅ Connection successful to service!
```

- The legend > This is the Python code that you just ran:

<details>
<summary>Show Python code</summary>

```python
# 4-direct-login.py
from radkit_client import Client
from radkit_common.rpc.client_transports.verify import RPCVerificationError # Specific exception for failed RPC verification
import getpass
import sys

server_address ="10.10.20.59"
RPC_PORT = 8181

if len(sys.argv) != 2:
	print("Usage: python scripts/4-direct-login.py <user_id>")
	sys.exit(1)

user_id = sys.argv[1]
e2ee_validation_token = getpass.getpass("🔑 Enter your E2EE validation token: ")

with Client.create() as client:
	service = client.service_direct(
		username=user_id,
		host=server_address,
		port=int(RPC_PORT),
		password=e2ee_validation_token
	)
	try:
		service.wait()
		print(f"✅ Connection successful to service!")
	except RPCVerificationError as e:
		print(f"🔥 Connection to service failed: {e}")
	except Exception as e:
		print(f"🔥 An unexpected error occurred while connecting to service: {e}")
```

</details>