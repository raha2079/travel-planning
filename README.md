# Travel Planning

A nanoagent plugin that validates AI agent performance on budget-constrained travel planning tasks. Tests whether an AI agent can correctly select a flight and hotel within a specified budget while respecting traveler preferences.

## Tools

The plugin provides tools for the `travel-planning` task:

- `load_request` - Load the travel request with origin, destination, budget, currency, and preferences
- `search_flights` - Search available flights and select the preferred flight ID
- `search_hotels` - Search available hotels in the destination city
- `check_budget` - Calculate total cost (flight + hotel × nights) and verify within budget

The reference tool (answer key, not available to agents):
- `validate_selection` - Validates the correct final booking selection

## Layout

```
travel-planning/
├── contract.py              # Type definitions (slimconfig Output classes)
├── nanoagent.yaml          # Plugin manifest
├── pyproject.toml          # Dependencies
├── uv.lock                 # Locked dependencies
├── run.sh                  # Environment validation script
├── src/plugin/             # Plugin implementation
│   ├── __main__.py         # MCP server entry point
│   ├── server.py           # MCP server
│   └── tools.py            # Tool implementations
├── verifier/               # Verification logic
│   ├── __init__.py         # verify_input, verify_output, verify_task
│   └── task.py             # Independent verifier (no LLM)
├── tests/                  # Test suite
│   ├── test_verifier.py    # Pytest tests
│   ├── *.json              # Test data
│   └── over_budget/        # Additional test cases
├── ui/                     # Result rendering
│   ├── renderers.js        # Output renderers
│   └── renderers.css       # Styling
└── product/                # RUSH Lab metadata
    ├── product.yaml        # Plugin catalog info
    └── icon.svg            # Plugin icon
```

## Develop and run

**Install dependencies:**

```bash
uv sync
```

**Run validation:**

```bash
./run.sh
```

**Test the verifier:**

```bash
python3 tests/test_verifier_standalone.py tests/output.json \
  --request tests/request.json \
  --options tests/options.json \
  --trace tests/action_trace.json
```

**Run pytest tests:**

```bash
uv run pytest tests/test_verifier.py -v
```

The verifier independently validates:
- Flight route matches origin → destination
- Hotel city matches destination
- Preferred flight ID was selected
- Hotel nights matches preference
- Budget calculation: flight_price + (hotel_nightly_price × nights)
- Total cost does not exceed budget
- Action trace contains exactly 5 events with complete evidence payloads

## Task Description

**Goal**: Select valid transport and lodging options within the requested budget.

**Input**:
- Travel request with origin, destination, budget, currency
- Preferences: specific flight_id and number of hotel_nights
- Available flights and hotels with prices

**Output**:
- Selected flight_id (must match preferred flight)
- Selected hotel_id (must be in destination city)
- Number of hotel_nights (must match preference)
- total_cost (flight + hotel × nights)
- currency

**Verification**: The verifier independently recalculates all costs and validates every constraint without using an LLM as judge.

## License

MIT License
