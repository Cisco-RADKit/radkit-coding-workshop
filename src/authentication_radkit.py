import os
from dotenv import load_dotenv

from radkit_client import Client
from radkit_client.sync import ClientStatus, ServiceStatus # Nice enums to get the status of the client and service

load_dotenv()

user_id = os.getenv("RADKIT_USER")
service_id = os.getenv("RADKIT_SERVICE")

with Client.create() as client:
    client.sso_login(user_id)
    print("✅ Authentication successful!") if client.status == ClientStatus.CONNECTED else print("🔥 Connection failed ...")
    
    service = client.service_cloud(service_id).wait()
    print(f"✅ Connection successful to service {service.service_id}!") if service.status == ServiceStatus.READY else print(f"🔥 Connection to service {service.service_id} failed ...")
    
    for device in service.inventory.values():
        print(f"📱 Device {device.name} is type {device.device_type} and has host {device.host} ...")