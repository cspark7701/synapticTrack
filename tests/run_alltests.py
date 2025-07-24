import pytest
import sys
from pathlib import Path

def main():
    # Define the root test directory (this script's directory)
    test_dir = Path(__file__).parent.resolve()
    
    # Run pytest on all tests in this directory
    result = pytest.main([
        str(test_dir),
        "--tb=short",          # optional: short traceback formatting
        "--color=yes",         # optional: colored output
        "-v"                   # optional: verbose mode
    ])

    # Exit with pytest's return code
    sys.exit(result)

if __name__ == "__main__":
    main()

