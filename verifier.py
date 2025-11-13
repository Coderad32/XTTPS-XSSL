# verifier.py
# Verifies certificate validity

import json
from datetime import datetime

class CertificateVerifier:
    def verify_chain(self, cert_json):
        try:
            cert = json.loads(cert_json)
            now = datetime.utcnow()
            valid_from = datetime.fromisoformat(cert["valid_from"])
            valid_to = datetime.fromisoformat(cert["valid_to"])
            return valid_from <= now <= valid_to
        except Exception:
            return False

