"""Type contracts for travel planning task."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated
from slimconfig import Output


class Tool(str, Enum):
    """Available tools."""
    LOAD_REQUEST = "load_request"
    SEARCH_FLIGHTS = "search_flights"
    SEARCH_HOTELS = "search_hotels"
    CHECK_BUDGET = "check_budget"
    VALIDATE_SELECTION = "validate_selection"


class Task(str, Enum):
    """Available tasks."""
    TRAVEL_PLANNING = "travel-planning"


# Tool Input/Output Contracts

@dataclass
class LoadRequestInput(Output):
    """Input for load_request tool."""
    pass


@dataclass
class LoadRequestOutput(Output):
    """Output from load_request tool."""
    origin: Annotated[str, "Origin city"]
    destination: Annotated[str, "Destination city"]
    budget: Annotated[float, "Total budget for trip"]
    currency: Annotated[str, "Currency code (e.g., USD)"]


@dataclass
class SearchFlightsInput(Output):
    """Input for search_flights tool."""
    pass


@dataclass
class SearchFlightsOutput(Output):
    """Output from search_flights tool."""
    flight_ids: Annotated[list[str], "List of all available flight IDs"]
    selected_flight_id: Annotated[str, "ID of the selected flight"]


@dataclass
class SearchHotelsInput(Output):
    """Input for search_hotels tool."""
    pass


@dataclass
class SearchHotelsOutput(Output):
    """Output from search_hotels tool."""
    hotel_ids: Annotated[list[str], "List of all available hotel IDs"]
    selected_hotel_id: Annotated[str, "ID of the selected hotel"]


@dataclass
class CheckBudgetInput(Output):
    """Input for check_budget tool."""
    pass


@dataclass
class CheckBudgetOutput(Output):
    """Output from check_budget tool with full calculation breakdown."""
    flight_price: Annotated[float, "Price of selected flight"]
    nightly_price: Annotated[float, "Hotel price per night"]
    hotel_nights: Annotated[int, "Number of hotel nights"]
    lodging_total: Annotated[float, "Total lodging cost (nightly_price × nights)"]
    total_cost: Annotated[float, "Total trip cost (flight + lodging)"]
    budget: Annotated[float, "Budget limit"]
    within_budget: Annotated[bool, "True if total_cost <= budget"]


@dataclass
class ValidateSelectionInput(Output):
    """Input for validate_selection tool."""
    pass


@dataclass
class ValidateSelectionOutput(Output):
    """Output from validate_selection tool."""
    flight_id: Annotated[str, "Selected flight ID"]
    hotel_id: Annotated[str, "Selected hotel ID"]
    hotel_nights: Annotated[int, "Number of hotel nights booked"]
    total_cost: Annotated[float, "Total trip cost"]
    currency: Annotated[str, "Currency code"]


# Task Input/Output Contracts

@dataclass
class TravelPlanningInput(Output):
    """Input for the travel planning task."""
    pass


@dataclass
class TravelPlanningOutput(Output):
    """Output from the travel planning task."""
    flight_id: Annotated[str, "Selected flight ID"]
    hotel_id: Annotated[str, "Selected hotel ID"]
    hotel_nights: Annotated[int, "Number of hotel nights"]
    total_cost: Annotated[float, "Total cost"]
    currency: Annotated[str, "Currency code"]


# Tool and Task Mappings

TOOLS = {
    Tool.LOAD_REQUEST: (LoadRequestInput, LoadRequestOutput),
    Tool.SEARCH_FLIGHTS: (SearchFlightsInput, SearchFlightsOutput),
    Tool.SEARCH_HOTELS: (SearchHotelsInput, SearchHotelsOutput),
    Tool.CHECK_BUDGET: (CheckBudgetInput, CheckBudgetOutput),
    Tool.VALIDATE_SELECTION: (ValidateSelectionInput, ValidateSelectionOutput),
}

TASKS = {
    Task.TRAVEL_PLANNING: (TravelPlanningInput, TravelPlanningOutput),
}
