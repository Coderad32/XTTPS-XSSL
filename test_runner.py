# test_runner.py
# CLI test runner for all modules

import unittest
import os

def discover_and_run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="crypto/tests", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    discover_and_run_tests()

