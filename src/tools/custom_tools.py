# src/tools/custom_tools.py

from pydantic import BaseModel, Field
from typing import List, Optional
import os
import json
import google.generativeai as genai
from .memory_tools import Memory_Retrieve, Memory_Update
from .doc_tools import DocumentGenerator

# 1. Output Schema for ItineraryParser
class ItineraryParserOutput(BaseModel):
    """Structured data extracted from raw itinerary text."""
    destination_iata: str = Field(..., description="IATA code of the final destination (e.g., DXB, SIN).")
    arrival_time_utc: str = Field(..., description="ISO 8601 timestamp of arrival time (e.g., 2026-01-10T14:00:00Z).")
    check_in_time_utc: str = Field(..., description="ISO 8601 timestamp of hotel check-in time.")
    raw_activities: List[str] = Field(..., description="List of major, unstructured activities mentioned (e.g., 'Desert Safari', 'Meeting').")
    valid_trip: bool = Field(default=True, description="True if input is a valid trip request, False if just chat.")

# 2. Itinerary Parser Tool Function
def ItineraryParser(raw_text: str) -> ItineraryParserOutput:
    """
    Parses unstructured text (email, chat message) to extract key trip details,
    making them machine-readable for the Planner Agent.
    Uses Gemini API for extraction if available, otherwise falls back to basic keyword matching.
    """
    print("--- Tool: ItineraryParser Executed ---")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"""
            Extract the following travel details from the text below:
            1. Destination IATA code (guess if not explicit, e.g. London -> LHR, Lucknow -> LKO).
            2. Arrival Time in ISO 8601 (UTC). If year is missing, assume 2025. If time missing, assume 12:00:00.
            3. Check-in Time in ISO 8601 (UTC). Assume 3 hours after arrival if not specified.
            4. List of activities mentioned.
            5. valid_trip: Boolean. True if the user is explicitly asking to plan a trip, mentioning a destination/date, OR modifying an existing plan (e.g. "change to Paris"). False if it's just a greeting (e.g. "hello", "hi") or a general question.
            
            Text: "{raw_text}"
            
            Return ONLY a JSON object with keys: destination_iata, arrival_time_utc, check_in_time_utc, raw_activities, valid_trip.
            """
            response = model.generate_content(prompt)
            cleaned = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            
            return ItineraryParserOutput(**data)
        except Exception as e:
            print(f"Parser LLM Error: {e}")
            
    # Fallback if API fails or not present
    is_valid = "plan" in raw_text.lower() or "trip" in raw_text.lower() or "go" in raw_text.lower()
    return ItineraryParserOutput(
        destination_iata="LKO" if "lucknow" in raw_text.lower() else "DXB",
        arrival_time_utc="2025-12-01T10:00:00Z",
        check_in_time_utc="2025-12-01T14:00:00Z",
        raw_activities=["General Sightseeing"],
        valid_trip=is_valid
    )

# 3. Weather API Tool Function (Needs a real API or mock)
def WeatherAPICall(location: str, date: str) -> str:
    """
    Fetches a simple summary of the 5-day weather forecast for a location.
    """
    print(f"--- Tool: WeatherAPICall Executed for {location} ---")
    # In a real app, we would use requests.get(f"api.openweathermap.org/...")
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