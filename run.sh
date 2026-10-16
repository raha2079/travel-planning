#!/usr/bin/env bash
# Template checks (required by RUSH Lab)
set -euo pipefail

echo "Running template checks..."

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Check uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv not found. Install from https://github.com/astral-sh/uv"
    exit 1
fi

# Check required files exist
for file in contract.py nanoagent.yaml pyproject.toml uv.lock; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file $file not found"
        exit 1
    fi
done

echo "Template checks passed."
echo ""

# Plugin-specific validation
echo "=== Travel Planning Plugin Environment Check ==="

# Check Python version
echo -n "Python version: "
python3 --version

# Check uv version
echo -n "uv version: "
uv --version

# Check required files
echo "Checking required files..."
required_files=(
    "contract.py"
    "nanoagent.yaml"
    "pyproject.toml"
    "src/plugin/__main__.py"
    "verifier/task.py"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (missing)"
        exit 1
    fi
done

# Run verifier tests
echo ""
echo "Running verifier tests..."
echo "Test 1: Golden case (should PASS)"
python3 tests/test_verifier_standalone.py tests/output.json \
    --request tests/request.json \
    --options tests/options.json \
    --trace tests/action_trace.json

echo ""
echo "Test 2: Bad budget (should FAIL)"
if python3 tests/test_verifier_standalone.py tests/bad_budget.json \
    --request tests/request.json \
    --options tests/options.json \
    --trace tests/action_trace.json; then
    echo "ERROR: Bad budget test should have failed!"
    exit 1
else
    echo "✓ Correctly rejected over-budget case"
fi

echo ""
echo "Test 3: Bad trace (should FAIL)"
if python3 tests/test_verifier_standalone.py tests/output.json \
    --request tests/request.json \
    --options tests/options.json \
    --trace tests/bad_trace.json; then
    echo "ERROR: Bad trace test should have failed!"
    exit 1
else
    echo "✓ Correctly rejected invalid trace"
fi

echo ""
echo "=== All checks passed! Plugin is ready. ==="
