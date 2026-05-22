#!/usr/bin/env python3
import subprocess
import sys


def run():
    print("Running tests with pytest...\n")
    p = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"], capture_output=True, text=True
    )
    print(p.stdout)
    if p.returncode == 0:
        print("\033[92m✅ All tests passed! Très bien.\033[0m")
    else:
        print("\033[91m❌ Some tests failed.\033[0m")
        print(p.stderr)
    return p.returncode


if __name__ == "__main__":
    raise SystemExit(run())
