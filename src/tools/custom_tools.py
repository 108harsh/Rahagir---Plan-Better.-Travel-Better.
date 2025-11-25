# src/tools/custom_tools.py

from pydantic import BaseModel, Field
from typing import List

# 1. Output Schema for ItineraryParser
class ItineraryParserOutput(BaseModel):
    """Structured data extracted from raw itinerary text."""
    destination_iata: str = Field(..., description="IATA code of the final destination (e.g., DXB).")
    arrival_time_utc: str = Field(..., description="ISO 8601 timestamp of arrival time.")
    check_in_time_utc: str
    raw_activities: List[str]

# 2. Itinerary Parser Tool Function
def ItineraryParser(raw_text: str) -> ItineraryParserOutput:
    """
    Parses unstructured text (email, note) to extract key trip details.
    This tool should use internal logic (e.g., regex, NLP) to extract required fields.
    """
    # NOTE: Actual implementation requires NLP/regex logic. Using a mock return for structure.
    print("--- Tool: ItineraryParser Executed ---")
    return ItineraryParserOutput(
        destination_iata="DXB",
        arrival_time_utc="2026-01-10T14:00:00Z",
        check_in_time_utc="2026-01-10T17:00:00Z",
        raw_activities=["Desert Safari on Jan 11th", "Laptop needed for work"]
    )

# 3. Weather API Tool Function (Needs a real API or mock)
def WeatherAPICall(location: str, date: str) -> str:
    """
    Fetches a simple summary of the 5-day weather forecast for a location.
    """
    print(f"--- Tool: WeatherAPICall Executed for {location} ---")
    return "Weather is forecast to be hot and clear, average 30°C. No rain expected, high UV index."

# GoogleSearch is assumed to be a built-in tool in the agent framework.
# src/tools/custom_tools.py (Continued)

# 4. Document Generator Tool Function
def DocumentGenerator(content: str, trip_id: str) -> str:
    """
    Generates a final, user-ready PDF/Markdown document (the travel guide) 
    containing the itinerary, packing list, and conflict resolution details.
    """
    print(f"--- Tool: DocumentGenerator Executed. Created PDF for {trip_id} ---")
    # NOTE: Implementation involves template rendering and file I/O.
    return "Document successfully created at /output/DXB-20260110-Guide.pdf"

# 5. Notification Manager Tool Function
def NotificationManager(message: str, time_offset: str) -> bool:
    """
    Sends a proactive, context-aware alert to the user's preferred channel (e.g., SMS/Email).
    """
    print(f"--- Tool: NotificationManager Executed. Scheduled alert for {time_offset} ---")
    # NOTE: Implementation involves integrating with a real alert service (Twilio, email API).
    return True