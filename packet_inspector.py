# packet_inspector.py
# Decodes and displays XTTP packets

import json

def inspect_packet(packet):
    print("=== XTTP Packet Inspector Pro/session ===")
    print("Headers:")
    for k, v in packet.get("headers", {}).items():
        print(f"  {k}: {v}")
    print("Payload:")
    print(packet.get("payload", "Optional ENCRYPTED META DATA"))
#
# I know this doesnt function and requires a new script to runtime.
#

import datetime
import uuid
import json
import binascii

def inspect_packet(packet, debug=False):
    session_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    print(f"=== XTTP Packet Inspector Pro/session ===")
    print(f"Session ID: {session_id}")
    print(f"Timestamp: {timestamp}")
    print("\nHeaders:")

    headers = packet.get("headers", {})
    if not headers:
        print("  [No headers found]")
    else:
        for k, v in headers.items():
            print(f"  {k:<20}: {v}")

    print("\nPayload:")
    payload = packet.get("payload", None)
    if payload is None:
        print("  [Missing or encrypted payload]")
    elif isinstance(payload, bytes):
        print(f"  Binary payload ({len(payload)} bytes)")
        if debug:
            print("  Hex Dump:")
            print("  " + binascii.hexlify(payload).decode())
    elif isinstance(payload, str):
        print(f"  Text payload ({len(payload)} chars)")
        if debug:
            print("  Raw content:")
            print(f"  {payload}")
    elif isinstance(payload, dict):
        print("  JSON payload:")
        print(json.dumps(payload, indent=2))
    else:
        print(f"  Unknown payload type: {type(payload)}")

    if debug:
        print("\n[Debug Mode Enabled]")
        print(f"Packet structure: {json.dumps(packet, indent=2)}")

# Example usage
if __name__ == "__main__":
    sample_packet = {
        "headers": {
            "Content-Type": "application/json",
            "X-Session-Token": "abc123xyz"
        },
        "payload": {"user": "cody (@coderad32 search)", "action": "login"}
    }
    inspect_packet(sample_packet, debug=True)