#!/usr/bin/env bash
# Exits 0 when this environment can run the plugin. NanoAgent runs it before every launch,
# with the environment the plugin will get.

set -euo pipefail

cd "$(dirname "$0")"

command -v uv >/dev/null || { echo "uv is not installed" >&2; exit 1; }

while IFS= read -r line || [[ -n "$line" ]]; do
    name="${line%%=*}"
    [[ -z "$name" || "$name" == \#* ]] && continue
    [[ -n "${!name:-}" ]] || { echo "$name is not set (declared in .env)" >&2; exit 1; }
done < .env

uv lock --check --offline --quiet || { echo "uv.lock is out of date with pyproject.toml" >&2; exit 1; }

# Travel Planning plugin checks
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
