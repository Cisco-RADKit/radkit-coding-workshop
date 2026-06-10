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