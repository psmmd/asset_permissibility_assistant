import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "validate_data.py"


def test_synthetic_data_is_consistent():
    result = subprocess.run([sys.executable, str(SCRIPT)], check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
