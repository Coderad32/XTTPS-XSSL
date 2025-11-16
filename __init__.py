# tests/__init__.py
# Placeholder for reliability and performance tests

# tests/__init__.py

# Optional: shared test fixtures or configuration
import logging

logging.basicConfig(level=logging.DEBUG)

# tests/__init__.py

# This file can be empty unless you need shared fixtures or setup


# tests/__init__.py

def normalize_string(s):
    return s.strip().lower()

# tests/test_init.py

import unittest
from tests import normalize_string

class TestInitHelpers(unittest.TestCase):
    def test_normalize_string(self):
        self.assertEqual(normalize_string("  Hello "), "hello")
        self.assertEqual(normalize_string("WORLD"), "world")
        self.assertEqual(normalize_string("  Mixed Case  "), "mixed case")

if __name__ == "__main__":
    unittest.main()

```
python -m unittest discover -s tests
```







`