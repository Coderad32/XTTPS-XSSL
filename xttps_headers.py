# xttp_headers.py
# Defines and validates custom XTTP headers

class HeaderValidator:
    REQUIRED_HEADERS = ["X-Session-ID", "X-Timestamp"]

    def validate(self, headers):
        for key in self.REQUIRED_HEADERS:
            if key not in headers:
                return False
        return True
#
# xttp_headers.py update && upgrade
#
import logging
from datetime import datetime, timedelta

class HeaderValidator:
    REQUIRED_HEADERS = ["X-Session-ID", "X-Timestamp"]
    OPTIONAL_HEADERS = ["X-Client-Hello", "X-Certificate", "X-Signature"]
    TIMESTAMP_TOLERANCE_SECONDS = 60  # Acceptable clock skew

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def validate(self, headers):
        self.logger.debug("Validating headers: %s", headers)

        # Check required headers
        missing = [key for key in self.REQUIRED_HEADERS if key not in headers]
        if missing:
            self.logger.warning("Missing required headers: %s", missing)
            return False

        # Validate timestamp freshness
        if not self._is_timestamp_valid(headers.get("X-Timestamp")):
            self.logger.warning("Invalid or expired timestamp")
            return False

        # Optional: Validate header types
        if not self._validate_types(headers):
            self.logger.warning("Header type mismatch")
            return False

        self.logger.info("Header validation passed")
        return True

    def _is_timestamp_valid(self, timestamp_str):
        try:
            ts = datetime.fromisoformat(timestamp_str)
            now = datetime.utcnow()
            delta = abs((now - ts).total_seconds())
            return delta <= self.TIMESTAMP_TOLERANCE_SECONDS
        except Exception as e:
            self.logger.error("Timestamp parsing failed: %s", e)
            return False

    def _validate_types(self, headers):
        # Example: enforce string types for all headers
        for key, value in headers.items():
            if not isinstance(value, str):
                self.logger.debug("Header %s has non-string value: %s", key, type(value))
                return False
        return True

    def list_missing_headers(self, headers):
        return [key for key in self.REQUIRED_HEADERS if key not in headers]

    def list_optional_headers_present(self, headers):
        return [key for key in self.OPTIONAL_HEADERS if key in headers]