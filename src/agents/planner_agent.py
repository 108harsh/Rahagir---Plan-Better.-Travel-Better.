# src/agents/planner_agent.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from ..tools.custom_tools import ItineraryParserOutput # Assuming Parser Output is defined in custom_tools

# --- 1. Structured Output Models (The Task Artifact) ---
class ConflictResolution(BaseModel):
    """Details a conflict identified and the proposed resolution."""
    original_conflict: str = Field(..., description="The logistical or temporal problem found (e.g., '3-hour gap between arrival and check-in').")
    recommended_action: str = Field(..., description="The top-ranked, actionable solution for mitigation (e.g., 'Draft email to hotel for early check-in').")
    
class PackingInput(BaseModel):
    """Synthesized environmental and compliance data for the Curation Agent."""
    weather_summary: str = Field(..., description="Concise summary of 5-day weather (e.g., 'Hot and clear, high UV index').")
    activities_tags: List[str] = Field(..., description="List of planned activities (e.g., ['Desert Safari', 'Business Meeting']).")
    compliance_tags: List[str] = Field(..., description="Required documents/rules (e.g., ['Visa Required', 'Type C Power Adapter']).")

class TaskArtifact(BaseModel):
    """The complete, structured output passed from the Planner Agent to the Curation Agent."""
    trip_id: str = Field(..., description="Unique ID for the trip (e.g., DXB-20260110).")
    itinerary_timeline: List[Dict[str, Any]] = Field(..., description="The clean, chronological list of scheduled events with local times.")
    conflict_resolutions: List[ConflictResolution] = Field(..., description="List of all conflicts found and the Planner's recommended solutions.")
    packing_inputs: PackingInput

# --- 2. The Planner Agent Class ---
class PlannerAgent:
    def __init__(self, llm_model, system_prompt):
        # Initialize the LLM client and model
        self.llm = llm_model 
        self.system_prompt = system_prompt
        
        # Tools: ItineraryParser (Custom), WeatherAPICall (Custom), GoogleSearch (Built-in)
        # Note: Tool list must be defined by the chosen framework
        self.tools = ['ItineraryParser', 'WeatherAPICall', 'GoogleSearch'] 

    def run_planning_cycle(self, raw_user_input: str) -> TaskArtifact:
        """
        Executes the planning cycle: parse input, resolve conflicts, generate structured output.
        """
        # 1. LLM uses ItineraryParser tool on raw_user_input.
        # 2. LLM reasons over output, identifies conflicts (e.g., arrival gap), and calls Weather/GoogleSearch.
        # 3. LLM compiles the final TaskArtifact object.
        
        # Placeholder logic (Replace with actual framework logic)
        print("--- Planner Agent: Running Planning Cycle ---")
        
        # The agent must ensure its final output conforms to the TaskArtifact schema.
        # return self.llm.process(prompt=raw_user_input, tools=self.tools, output_schema=TaskArtifact)
        
        # Returning a mock TaskArtifact for structure demonstration:
        return TaskArtifact(
            trip_id="DXB-20260110",
            itinerary_timeline=[{"event": "Flight Arrival", "time": "14:00"}, {"event": "Hotel Check-in", "time": "17:00"}],
            conflict_resolutions=[
                ConflictResolution(original_conflict="3-hour gap after flight arrival.", recommended_action="Draft email to hotel for early check-in.")
            ],
            packing_inputs=PackingInput(
                weather_summary="Hot and clear, high UV index.", 
                activities_tags=["Desert Safari", "Business"],
                compliance_tags=["Visa Required", "Type C Power Adapter"]
            )
        )