import tempfile
import os
import uuid

def generate_warp_config(user_id):
    """
    Generate fake WireGuard config (replace later with real wgcf)
    """
    unique_id = str(uuid.uuid4())[:8]

    config_data = f"""
[Interface]
PrivateKey = PRIVATE_KEY_{unique_id}
Address = 172.16.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = PUBLIC_KEY_{unique_id}
AllowedIPs = 0.0.0.0/0
Endpoint = engage.cloudflareclient.com:2408
"""

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".conf")
    temp_file.write(config_data.encode())
    temp_file.close()

    return temp_file.name, config_data
