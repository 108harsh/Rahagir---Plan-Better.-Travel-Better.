# src/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# --- 1. Planner Agent / Task Artifact Models (from planner_agent.py) ---

class ConflictResolution(BaseModel):
    """Details a conflict identified and the proposed resolution."""
    original_conflict: str = Field(..., description="The logistical or temporal problem found.")
    recommended_action: str = Field(..., description="The top-ranked, actionable solution for mitigation.")
    
class PackingInput(BaseModel):
    """Synthesized environmental and compliance data for the Curation Agent."""
    weather_summary: str = Field(..., description="Concise summary of 5-day weather.")
    activities_tags: List[str] = Field(..., description="List of planned activities.")
    compliance_tags: List[str] = Field(..., description="Required documents/rules.")

class TaskArtifact(BaseModel):
    """The complete, structured output passed from the Planner Agent to the Curation Agent."""
    trip_id: str = Field(..., description="Unique ID for the trip, or 'CHAT' if just conversation.")
    itinerary_timeline: List[Dict[str, Any]] = Field(default=[], description="The clean, chronological list of scheduled events.")
    conflict_resolutions: List[ConflictResolution] = Field(default=[], description="List of all conflicts found and the Planner's recommended solutions.")
    packing_inputs: Optional[PackingInput] = None
    follow_up_questions: List[str] = Field(default=[], description="Questions to ask the user for clarification or next steps.")
    chat_response: Optional[str] = Field(default=None, description="Conversational response if no trip is planned.")

# --- 2. Loop Monitor Agent Models (from loop_monitor_agent.py) ---

class TriggerThreshold(BaseModel):
    """Defines the specific condition that forces a re-plan."""
    delay_minutes: int = Field(60)
    weather_severity: str = Field("Sandstorm")

class CriticalCheckpoint(BaseModel):
    """An individual event the Loop Agent must continuously poll."""
    check_type: str = Field(..., description="e.g., 'Flight_Status', 'Severe_Weather_Alert'.")
    location: str = Field(..., description="IATA code or address of the checkpoint.")
    trigger_threshold: TriggerThreshold

class MonitoringConfig(BaseModel):
    """The complete configuration passed to the Adaptation Monitor Agent."""
    trip_id: str
    monitoring_interval_min: int = Field(30)
    critical_checkpoints: List[CriticalCheckpoint]