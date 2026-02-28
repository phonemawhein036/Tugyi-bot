def generate_wireguard_config(user_id):
    return f"""
[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 172.16.0.{user_id % 250}/32
DNS = 1.1.1.1

[Peer]
PublicKey = YOUR_PUBLIC_KEY
AllowedIPs = 0.0.0.0/0
Endpoint = 162.159.192.10:500
PersistentKeepalive = 25
"""
