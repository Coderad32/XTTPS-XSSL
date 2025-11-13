# issuer.py
# Issues XSSL certificates

import json
import uuid
from datetime import datetime, timedelta

class CertificateIssuer:
    def issue_certificate(self, subject):
        cert = {
            "subject": subject,
            "issuer": "XSSL-CA",
            "valid_from": datetime.utcnow().isoformat(),
            "valid_to": (datetime.utcnow() + timedelta(days=365)).isoformat(),
            "signature": str(uuid.uuid4())
        }
        return json.dumps(cert, indent=2)

