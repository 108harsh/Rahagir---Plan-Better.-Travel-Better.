# src/agents/planner_agent.py

# CORRECT IMPORT: Pulls all models from the central file
from src.models import TaskArtifact, ConflictResolution, PackingInput
from ..tools.custom_tools import ItineraryParserOutput # Assuming Parser Output is defined in custom_tools
from typing import List, Dict, Any

# --- 2. The Planner Agent Class ---
class PlannerAgent:
    def __init__(self, llm_model, system_prompt):
        self.llm = llm_model 
        self.system_prompt = system_prompt
        
        # Tools: ItineraryParser (Custom), WeatherAPICall (Custom), GoogleSearch (Built-in)
        self.tools = ['ItineraryParser', 'WeatherAPICall', 'GoogleSearch'] 

    def run_planning_cycle(self, raw_user_input: str) -> TaskArtifact:
        """
        Executes the planning cycle: parse input, resolve conflicts, generate structured output.
        """
        print("--- Planner Agent: Running Planning Cycle ---")
        
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