# run_alltests.py
import pytest
import sys
from pathlib import Path

def main():
    # Ensure test_dir points to the directory containing this script
    test_dir = Path(__file__).resolve().parent

    # Set working directory to the repo root to ensure relative paths in tests work
    repo_root = test_dir.parent
    sys.path.insert(0, str(repo_root))  # Optional: to import src modules
    os.chdir(repo_root)

    # Run pytest starting from the test directory
    result = pytest.main([
        str(test_dir),
        "--tb=short",    # short tracebacks
        "--color=yes",   # colored output
        "-v"             # verbose output
    ])
    sys.exit(result)

if __name__ == "__main__":
    import os
    main()

