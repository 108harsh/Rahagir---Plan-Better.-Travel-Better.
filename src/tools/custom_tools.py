# src/tools/custom_tools.py

from pydantic import BaseModel, Field
from typing import List, Optional
from .memory_tools import Memory_Retrieve, Memory_Update
from .doc_tools import DocumentGenerator

# 1. Output Schema for ItineraryParser
class ItineraryParserOutput(BaseModel):
    """Structured data extracted from raw itinerary text."""
    destination_iata: str = Field(..., description="IATA code of the final destination (e.g., DXB, SIN).")
    arrival_time_utc: str = Field(..., description="ISO 8601 timestamp of arrival time (e.g., 2026-01-10T14:00:00Z).")
    check_in_time_utc: str = Field(..., description="ISO 8601 timestamp of hotel check-in time.")
    raw_activities: List[str] = Field(..., description="List of major, unstructured activities mentioned (e.g., 'Desert Safari', 'Meeting').")

# 2. Itinerary Parser Tool Function
def ItineraryParser(raw_text: str) -> ItineraryParserOutput:
    """
    Parses unstructured text (email, chat message) to extract key trip details,
    making them machine-readable for the Planner Agent.
    """
    print("--- Tool: ItineraryParser Executed ---")
    
    # NOTE: We use simple string matching here to simulate successful parsing 
    # based on your previous input for testing the overall flow.
    if "Dubai" in raw_text or "DXB" in raw_text:
        return ItineraryParserOutput(
            destination_iata="DXB",
            arrival_time_utc="2026-01-10T14:00:00Z",
            check_in_time_utc="2026-01-10T17:00:00Z",
            raw_activities=["Desert Safari on Jan 11th", "Laptop needed for work"]
        )
    else:
        # Default or failure case
        return ItineraryParserOutput(
            destination_iata="N/A",
            arrival_time_utc="N/A",
            check_in_time_utc="N/A",
            raw_activities=[]
        )

# 3. Weather API Tool Function (Needs a real API or mock)
def WeatherAPICall(location: str, date: str) -> str:
    """
    Fetches a simple summary of the 5-day weather forecast for a location.
    """
    print(f"--- Tool: WeatherAPICall Executed for {location} ---")
    return "Weather is forecast to be hot and clear, average 30°C. No rain expected, high UV index."

# 4. Notification Manager Tool Function
def NotificationManager(message: str, time_offset: str) -> bool:
    """
    Sends a proactive, context-aware alert to the user's preferred channel (e.g., SMS/Email).
    """
    print(f"--- Tool: NotificationManager Executed. Scheduled alert for {time_offset} ---")
    return True

def TaskScheduler(task_description: str, time: str) -> bool:
    """
    Integrates with the user's external calendar or to-do app to schedule 
    a specific task (e.g., 'Take Medication', 'Print Document').
    """
    print(f"--- Tool: TaskScheduler Executed. Scheduled '{task_description}' for {time} ---")
    return True