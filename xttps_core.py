# xttps_core.py
# Manages session lifecycle, handshake, and packet parsing

import uuid
import time
from .xttp_headers import HeaderValidator

class Session:
    def __init__(self, client_id):
        self.session_id = str(uuid.uuid4())
        self.client_id = client_id
        self.start_time = time.time()
        self.handshake_complete = False

    def perform_handshake(self, client_hello):
        # Simulate handshake logic
        if "X-Client-Hello" in client_hello:
            self.handshake_complete = True
            return {"X-Server-Hello": self.session_id}
        return {"error": "Invalid handshake"}

    def parse_packet(self, packet):
        if not self.handshake_complete:
            raise Exception("Handshake not completed")
        headers = packet.get("headers", {})
        payload = packet.get("payload", "")
        if not HeaderValidator().validate(headers):
            raise Exception("Invalid headers")
        return f"Payload received: {payload}"

