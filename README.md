# Travel Planning Plugin

A nanoagent plugin that validates AI agent performance on budget-constrained travel planning tasks.

## Overview

This plugin tests whether an AI agent can correctly select a flight and hotel within a specified budget while respecting traveler preferences. The task requires:

- Selecting the preferred flight from available options
- Choosing a hotel in the destination city that fits the remaining budget
- Booking the exact number of hotel nights requested
- Independently calculating and verifying the total cost
- Following a specific workflow with verifiable evidence

## Task Description

**Goal**: Select valid transport and lodging options within the requested budget.

**Input**:
- Travel request with origin, destination, budget, currency
- Preferences: specific `flight_id` and number of `hotel_nights`
- Available flights and hotels with prices

**Output**:
- Selected `flight_id` (must match preferred flight)
- Selected `hotel_id` (must be in destination city)
- Number of `hotel_nights` (must match preference)
- `total_cost` (flight + hotel × nights)
- `currency`

## Workflow

The agent must call tools in this exact order:

1. **load_request** - Get travel request details
2. **search_flights** - Search and select the preferred flight
3. **search_hotels** - Search and select a hotel in the destination
4. **check_budget** - Calculate total cost with full breakdown
5. **validate_selection** - Confirm final booking details

## Verification

The verifier (`verifier/task.py`) independently validates:

### Schema Validation
- All required fields present with correct types
- Numeric values are finite and within bounds (0 to 1B)
- Hotel nights between 1 and 365

### Business Logic
- Flight route matches origin → destination
- Hotel city matches destination
- Preferred flight ID was selected
- Hotel nights matches preference
- Currency matches request

### Budget Calculation
- Independently recalculates: `flight_price + (hotel_nightly_price × nights)`
- Verifies total does not exceed budget
- Checks exact equality with reported total_cost

### Action Trace
Requires exactly 5 events with complete evidence payloads:

1. `load_request` - {origin, destination, budget, currency}
2. `search_flights` - {flight_ids: [all IDs], selected_flight_id}
3. `search_hotels` - {hotel_ids: [all IDs], selected_hotel_id}
4. `check_budget` - {flight_price, nightly_price, hotel_nights, lodging_total, total_cost, budget, within_budget}
5. `validate_selection` - {flight_id, hotel_id, hotel_nights, total_cost, currency}

## Installation

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd travel-planning

# Install dependencies
uv sync

# Run tests
uv run pytest tests/test_verifier.py
```

## Usage

### Running the Plugin

```bash
# Start the MCP server
uv run --frozen python -m plugin
```

### Testing with Sample Data

The `tests/` directory contains:
- `request.json` - Sample travel request
- `options.json` - Available flights and hotels
- `action_trace.json` - Expected workflow trace
- `output.json` - Expected output (golden case)
- `bad_budget.json` - Over-budget test case
- `bad_trace.json` - Invalid trace test case
- `over_budget/` - Additional over-budget scenarios

### Running the Verifier

```bash
# Verify a result
python verifier/task.py tests/output.json \
  --request tests/request.json \
  --options tests/options.json \
  --trace tests/action_trace.json
```

Expected output for valid case: `PASS`
Expected output for invalid case: `FAIL` with error details

## Test Cases

### Golden Case
- Budget: $1800 USD
- Preferred flight: fl-2 ($720)
- Hotel: ht-1 ($280/night)
- Nights: 3
- Total: $1560 (within budget) ✓

### Over-Budget Case
- Same preferences but with lower budget
- Verifier correctly rejects as exceeding budget ✗

### Invalid Trace Case
- Missing or incorrect action trace events
- Verifier rejects for incomplete workflow ✗

## Plugin Structure

```
travel-planning/
├── contract.py              # Type definitions for tools and tasks
├── nanoagent.yaml          # Plugin manifest
├── pyproject.toml          # Python dependencies
├── README.md               # This file
├── src/plugin/
│   ├── __init__.py
│   ├── __main__.py         # MCP server entry point
│   ├── server.py           # MCP server implementation
│   └── tools.py            # Tool implementations
├── verifier/
│   └── task.py             # Independent verifier (no LLM)
└── tests/
    ├── test_verifier.py    # Pytest test suite
    ├── request.json        # Sample request
    ├── options.json        # Sample options
    ├── action_trace.json   # Golden trace
    ├── output.json         # Golden output
    ├── bad_budget.json     # Failure case
    ├── bad_trace.json      # Failure case
    └── over_budget/        # Additional test scenarios
```

## Key Features

### Deterministic Verification
- No LLM as judge
- Mathematical calculation verification
- Exact schema and workflow validation
- Reproducible results

### Comprehensive Testing
- Positive test cases (valid bookings)
- Negative test cases (over budget, wrong preferences)
- Boundary cases (maximum values, edge cases)
- Trace validation (workflow correctness)

### Structured I/O
- All inputs and outputs use typed dataclasses
- Clear contracts defined in `contract.py`
- Validation at every step

## Development

### Adding New Test Cases

1. Create test data files in `tests/` directory
2. Add test function in `tests/test_verifier.py`
3. Run tests: `uv run pytest tests/test_verifier.py -v`

### Modifying the Verifier

The verifier is intentionally strict and validates:
- Input schemas
- Business logic constraints
- Budget calculations
- Workflow trace completeness

Any changes should maintain or increase strictness.

## Publishing to RUSH Lab

1. Ensure all tests pass locally
2. Push to GitHub repository
3. Sign in to [RUSH Lab](https://rush-lab.org)
4. Submit plugin to marketplace
5. Fix any packaging errors reported by marketplace checks

## License

MIT License

## Authors

Created for COMP 480/580 Fall 2026 Project Milestone
