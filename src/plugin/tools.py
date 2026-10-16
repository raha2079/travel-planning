"""Tool implementations for travel planning."""

import json
from pathlib import Path
from dataclasses import dataclass, asdict

# State management for the workflow
_state = {
    "request": None,
    "options": None,
    "selected_flight": None,
    "selected_hotel": None,
    "action_trace": [],
}


def _load_data():
    """Load request and options data from workspace."""
    workspace = Path("workspace")

    # Try to load from task input files
    request_file = workspace / "request.json"
    options_file = workspace / "options.json"

    if request_file.exists():
        with open(request_file) as f:
            _state["request"] = json.load(f)

    if options_file.exists():
        with open(options_file) as f:
            data = json.load(f)
            _state["request"] = data.get("request", _state["request"])
            _state["options"] = data.get("options", {})


def _add_action(action: str, data: dict):
    """Add an action to the trace."""
    _state["action_trace"].append({
        "action": action,
        "data": data
    })


def _save_trace():
    """Save action trace to workspace."""
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)

    with open(workspace / "action_trace.json", "w") as f:
        json.dump(_state["action_trace"], f, indent=2)


def _save_output(output: dict):
    """Save final output to workspace."""
    workspace = Path("workspace")
    workspace.mkdir(exist_ok=True)

    with open(workspace / "output.json", "w") as f:
        json.dump(output, f, indent=2)


def load_request() -> dict:
    """Load the travel request."""
    # Load data if not already loaded
    if _state["request"] is None:
        _load_data()

    if _state["request"] is None:
        raise ValueError("No request data available")

    req = _state["request"]

    # Add to action trace
    _add_action("load_request", {
        "origin": req["origin"],
        "destination": req["destination"],
        "budget": req["budget"],
        "currency": req["currency"],
    })
    _save_trace()

    return {
        "origin": req["origin"],
        "destination": req["destination"],
        "budget": req["budget"],
        "currency": req["currency"],
    }


def search_flights() -> dict:
    """Search flights and select the preferred one."""
    if _state["request"] is None or _state["options"] is None:
        _load_data()

    if _state["request"] is None or _state["options"] is None:
        raise ValueError("Must call load_request first")

    req = _state["request"]
    opts = _state["options"]

    # Get preferences
    preferred_flight_id = req["preferences"]["flight_id"]

    # Get available flights
    flights = opts.get("flights", [])
    flight_ids = [f["id"] for f in flights]

    # Find and select the preferred flight
    selected = None
    for flight in flights:
        if flight["id"] == preferred_flight_id:
            selected = flight
            break

    if selected is None:
        raise ValueError(f"Preferred flight {preferred_flight_id} not found")

    _state["selected_flight"] = selected

    # Add to action trace
    _add_action("search_flights", {
        "flight_ids": flight_ids,
        "selected_flight_id": selected["id"],
    })
    _save_trace()

    return {
        "flight_ids": flight_ids,
        "selected_flight_id": selected["id"],
    }


def search_hotels() -> dict:
    """Search hotels and select one."""
    if _state["request"] is None or _state["options"] is None:
        raise ValueError("Must call load_request and search_flights first")

    if _state["selected_flight"] is None:
        raise ValueError("Must call search_flights first")

    req = _state["request"]
    opts = _state["options"]

    # Get available hotels
    hotels = opts.get("hotels", [])
    hotel_ids = [h["id"] for h in hotels]

    # Filter hotels in destination city
    destination = req["destination"]
    destination_hotels = [h for h in hotels if h["city"] == destination]

    if not destination_hotels:
        raise ValueError(f"No hotels found in {destination}")

    # Calculate budget constraints
    flight_price = _state["selected_flight"]["price"]
    budget = req["budget"]
    hotel_nights = req["preferences"]["hotel_nights"]

    remaining_budget = budget - flight_price
    max_nightly_price = remaining_budget / hotel_nights

    # Select first hotel that fits budget
    selected = None
    for hotel in destination_hotels:
        if hotel["nightly_price"] <= max_nightly_price:
            selected = hotel
            break

    # If no hotel fits, select cheapest (will fail budget check)
    if selected is None:
        selected = min(destination_hotels, key=lambda h: h["nightly_price"])

    _state["selected_hotel"] = selected

    # Add to action trace
    _add_action("search_hotels", {
        "hotel_ids": hotel_ids,
        "selected_hotel_id": selected["id"],
    })
    _save_trace()

    return {
        "hotel_ids": hotel_ids,
        "selected_hotel_id": selected["id"],
    }


def check_budget() -> dict:
    """Calculate total cost and check budget."""
    if _state["request"] is None:
        raise ValueError("Must call load_request first")
    if _state["selected_flight"] is None:
        raise ValueError("Must call search_flights first")
    if _state["selected_hotel"] is None:
        raise ValueError("Must call search_hotels first")

    req = _state["request"]
    flight = _state["selected_flight"]
    hotel = _state["selected_hotel"]

    # Get values
    flight_price = flight["price"]
    nightly_price = hotel["nightly_price"]
    hotel_nights = req["preferences"]["hotel_nights"]
    budget = req["budget"]

    # Calculate totals
    lodging_total = nightly_price * hotel_nights
    total_cost = flight_price + lodging_total
    within_budget = total_cost <= budget

    # Add to action trace with full breakdown
    _add_action("check_budget", {
        "flight_price": flight_price,
        "nightly_price": nightly_price,
        "hotel_nights": hotel_nights,
        "lodging_total": lodging_total,
        "total_cost": total_cost,
        "budget": budget,
        "within_budget": within_budget,
    })
    _save_trace()

    return {
        "flight_price": flight_price,
        "nightly_price": nightly_price,
        "hotel_nights": hotel_nights,
        "lodging_total": lodging_total,
        "total_cost": total_cost,
        "budget": budget,
        "within_budget": within_budget,
    }


def validate_selection() -> dict:
    """Validate the final selection."""
    if _state["request"] is None:
        raise ValueError("Must call load_request first")
    if _state["selected_flight"] is None:
        raise ValueError("Must call search_flights first")
    if _state["selected_hotel"] is None:
        raise ValueError("Must call search_hotels first")

    req = _state["request"]
    flight = _state["selected_flight"]
    hotel = _state["selected_hotel"]

    # Calculate final values
    hotel_nights = req["preferences"]["hotel_nights"]
    total_cost = flight["price"] + (hotel["nightly_price"] * hotel_nights)

    # Create final output
    output = {
        "flight_id": flight["id"],
        "hotel_id": hotel["id"],
        "hotel_nights": hotel_nights,
        "total_cost": total_cost,
        "currency": req["currency"],
    }

    # Add to action trace
    _add_action("validate_selection", output)
    _save_trace()

    # Save final output
    _save_output(output)

    return output
