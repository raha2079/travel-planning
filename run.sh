#!/usr/bin/env bash
# Environment validation script for travel planning plugin

set -euo pipefail

echo "=== Travel Planning Plugin Environment Check ==="

# Check Python version
echo -n "Python version: "
python3 --version

# Check uv is installed
echo -n "uv version: "
if command -v uv &> /dev/null; then
    uv --version
else
    echo "ERROR: uv not found. Install from https://github.com/astral-sh/uv"
    exit 1
fi

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
python3 verifier/task.py tests/output.json \
    --request tests/request.json \
    --options tests/options.json \
    --trace tests/action_trace.json

echo ""
echo "Test 2: Bad budget (should FAIL)"
if python3 verifier/task.py tests/bad_budget.json \
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
if python3 verifier/task.py tests/output.json \
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
