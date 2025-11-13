# xttp_headers.py
# Defines and validates custom XTTP headers

class HeaderValidator:
    REQUIRED_HEADERS = ["X-Session-ID", "X-Timestamp"]

    def validate(self, headers):
        for key in self.REQUIRED_HEADERS:
            if key not in headers:
                return False
        return True

