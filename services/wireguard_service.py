from config import ENDPOINT, DNS

def generate_wireguard_config(user_id):
    return f"""
[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 172.16.0.{user_id % 250}/32
DNS = {DNS}

[Peer]
PublicKey = YOUR_PUBLIC_KEY
AllowedIPs = 0.0.0.0/0
Endpoint = {ENDPOINT}
PersistentKeepalive = 25
"""
