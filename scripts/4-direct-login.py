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