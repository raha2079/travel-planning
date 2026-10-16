"""Tests for travel planning verifier."""

import json
import subprocess
import sys
from pathlib import Path

def test_golden_case():
    """Test the golden/passing case."""
    test_dir = Path(__file__).parent
    verifier = test_dir.parent / "verifier" / "task.py"

    result = subprocess.run(
        [
            sys.executable,
            str(verifier),
            str(test_dir / "output.json"),
            "--request", str(test_dir / "request.json"),
            "--options", str(test_dir / "options.json"),
            "--trace", str(test_dir / "action_trace.json"),
        ],
        capture_output=True,
        text=True,
    )

    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Errors: {result.stderr}")

    assert result.returncode == 0, f"Verifier failed: {result.stdout}"
    assert "PASS" in result.stdout, f"Expected PASS, got: {result.stdout}"


def test_bad_budget():
    """Test over-budget case."""
    test_dir = Path(__file__).parent
    verifier = test_dir.parent / "verifier" / "task.py"

    result = subprocess.run(
        [
            sys.executable,
            str(verifier),
            str(test_dir / "bad_budget.json"),
            "--request", str(test_dir / "request.json"),
            "--options", str(test_dir / "options.json"),
            "--trace", str(test_dir / "action_trace.json"),
        ],
        capture_output=True,
        text=True,
    )

    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")

    assert result.returncode != 0, "Verifier should fail for over-budget case"
    assert "FAIL" in result.stdout, f"Expected FAIL, got: {result.stdout}"


def test_bad_trace():
    """Test invalid action trace case."""
    test_dir = Path(__file__).parent
    verifier = test_dir.parent / "verifier" / "task.py"

    result = subprocess.run(
        [
            sys.executable,
            str(verifier),
            str(test_dir / "output.json"),
            "--request", str(test_dir / "request.json"),
            "--options", str(test_dir / "options.json"),
            "--trace", str(test_dir / "bad_trace.json"),
        ],
        capture_output=True,
        text=True,
    )

    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")

    assert result.returncode != 0, "Verifier should fail for bad trace"
    assert "FAIL" in result.stdout, f"Expected FAIL, got: {result.stdout}"


if __name__ == "__main__":
    print("Running test_golden_case...")
    test_golden_case()
    print("\nRunning test_bad_budget...")
    test_bad_budget()
    print("\nRunning test_bad_trace...")
    test_bad_trace()
    print("\nAll tests passed!")
