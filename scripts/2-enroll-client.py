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