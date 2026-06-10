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