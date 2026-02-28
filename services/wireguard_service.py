import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization
from config import ENDPOINT, DNS


# 🔐 Generate WireGuard Key Pair
def generate_keypair():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    private_b64 = base64.b64encode(private_bytes).decode()
    public_b64 = base64.b64encode(public_bytes).decode()

    return private_b64, public_b64


# ⚡ Generate WireGuard Config (Auto New Each Time)
def generate_wireguard_config(user_id):
    private_key, public_key = generate_keypair()

    return f"""
[Interface]
PrivateKey = {private_key}
Address = 172.16.0.{user_id % 250}/32
DNS = {DNS}

[Peer]
PublicKey = {public_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {ENDPOINT}
PersistentKeepalive = 25
"""
