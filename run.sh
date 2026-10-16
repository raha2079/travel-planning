#!/usr/bin/env bash
# Environment validation script

set -euo pipefail

# Template checks (required)
command -v uv >/dev/null || { echo "uv is not installed" >&2; exit 1; }

if [[ -f .env ]]; then
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$key" ]] && continue
        # Check if variable is set in environment
        if [[ -z "${!key:-}" ]]; then
            echo "Environment variable $key is not set" >&2
            exit 1
        fi
    done < .env
fi

uv sync --frozen --quiet || { echo "uv.lock is out of date with pyproject.toml" >&2; exit 1; }

# Plugin-specific checks
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
