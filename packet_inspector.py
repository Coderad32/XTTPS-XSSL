# packet_inspector.py
# Decodes and displays XTTP packets

import json

def inspect_packet(packet):
    print("=== XTTP Packet Inspector ===")
    print("Headers:")
    for k, v in packet.get("headers", {}).items():
        print(f"  {k}: {v}")
    print("Payload:")
    print(packet.get("payload", ""))

