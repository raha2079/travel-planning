"""Type contracts for travel planning task.

This module defines the structured input and output types for all tools and tasks
in the travel planning plugin, following nanoagent's structured I/O principle.
"""

from dataclasses import dataclass
from enum import Enum


class Tool(str, Enum):
    """Available tools for travel planning workflow."""
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
class LoadRequestInput:
    """Input for load_request tool (no parameters needed)."""
    pass


@dataclass
class LoadRequestOutput:
    """Output from load_request tool."""
    origin: str
    destination: str
    budget: float
    currency: str


@dataclass
class SearchFlightsInput:
    """Input for search_flights tool (no parameters needed)."""
    pass


@dataclass
class SearchFlightsOutput:
    """Output from search_flights tool."""
    flight_ids: list[str]
    selected_flight_id: str


@dataclass
class SearchHotelsInput:
    """Input for search_hotels tool (no parameters needed)."""
    pass


@dataclass
class SearchHotelsOutput:
    """Output from search_hotels tool."""
    hotel_ids: list[str]
    selected_hotel_id: str


@dataclass
class CheckBudgetInput:
    """Input for check_budget tool (no parameters needed)."""
    pass


@dataclass
class CheckBudgetOutput:
    """Output from check_budget tool with full calculation breakdown."""
    flight_price: float
    nightly_price: float
    hotel_nights: int
    lodging_total: float
    total_cost: float
    budget: float
    within_budget: bool


@dataclass
class ValidateSelectionInput:
    """Input for validate_selection tool (no parameters needed)."""
    pass


@dataclass
class ValidateSelectionOutput:
    """Output from validate_selection tool."""
    flight_id: str
    hotel_id: str
    hotel_nights: int
    total_cost: float
    currency: str


# Task Input Contract

@dataclass
class TravelPlanningInput:
    """Input for the travel planning task."""
    # These fields will be provided by the nanoagent framework
    # and made available to tools through the plugin context


# Tool and Task Mappings

TOOLS = {
    Tool.LOAD_REQUEST: (LoadRequestInput, LoadRequestOutput),
    Tool.SEARCH_FLIGHTS: (SearchFlightsInput, SearchFlightsOutput),
    Tool.SEARCH_HOTELS: (SearchHotelsInput, SearchHotelsOutput),
    Tool.CHECK_BUDGET: (CheckBudgetInput, CheckBudgetOutput),
    Tool.VALIDATE_SELECTION: (ValidateSelectionInput, ValidateSelectionOutput),
}

TASKS = {
    Task.TRAVEL_PLANNING: TravelPlanningInput,
}
