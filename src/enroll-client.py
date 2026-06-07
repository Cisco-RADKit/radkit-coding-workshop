#
# Usage: python 001-enroll-client.py (using your virtual environment with the Radkit Client API installed)
#
# This example demonstrates how to enroll a client to non-interactive cloud authentication using the Radkit Client API.
# The client will be enrolled after a successful SSO login, allowing it to authenticate with the cloud without user interaction in future sessions.
#
# It cannot be executed on a Jupyter notebook because it requires console input, which is not compatible with the notebook environment.
#

import os
from dotenv import load_dotenv
from radkit_client import Client
from radkit_client.sync import ClientStatus

load_dotenv()

user_id = os.getenv("RADKIT_USER")

with Client.create() as client:
    client.sso_login(user_id)
    if client.status == ClientStatus.CONNECTED:
        client.enroll_client() # Enroll the client to non-interactive cloud authentication (blocking call)