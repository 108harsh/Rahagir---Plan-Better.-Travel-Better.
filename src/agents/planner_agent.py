# src/agents/planner_agent.py

# CORRECT IMPORT: Pulls all models from the central file
from src.models import TaskArtifact, ConflictResolution, PackingInput
from ..tools.custom_tools import ItineraryParserOutput, ItineraryParser # Assuming Parser Output is defined in custom_tools
from typing import List, Dict, Any
import os
import google.generativeai as genai
import json

# --- 2. The Planner Agent Class ---
class PlannerAgent:
    def __init__(self, llm_model, system_prompt):
        self.llm = llm_model 
        self.system_prompt = system_prompt
        
        # Tools: ItineraryParser (Custom), WeatherAPICall (Custom), GoogleSearch (Built-in)
        self.tools = ['ItineraryParser', 'WeatherAPICall', 'GoogleSearch'] 
        
        # Initialize Gemini if key is present
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("PlannerAgent: Connected to Gemini API.")
        else:
            print("PlannerAgent: No API Key found. Using MOCK mode.")

    def run_planning_cycle(self, raw_user_input: str) -> TaskArtifact:
        """
        Executes the planning cycle: parse input, resolve conflicts, generate structured output.
        """
        print("--- Planner Agent: Running Planning Cycle ---")
        
        # 1. Parse Input (using tool)
        parsed_data = ItineraryParser(raw_user_input)
        
        if self.api_key:
            try:
                # Real LLM Call
                prompt = f"""
                {self.system_prompt}
                
                User Input: {raw_user_input}
                Parsed Data: {parsed_data.json()}
                
                Identify potential conflicts (e.g., tight connections, missing visa) and suggest resolutions.
                Also provide packing tips based on the destination ({parsed_data.destination_iata}).
                
                Return the result ONLY as a JSON object matching the TaskArtifact structure:
                {{
                    "trip_id": "str",
                    "itinerary_timeline": [{{"event": "str", "time": "str"}}],
                    "conflict_resolutions": [{{"original_conflict": "str", "recommended_action": "str"}}],
                    "packing_inputs": {{
                        "weather_summary": "str",
                        "activities_tags": ["str"],
                        "compliance_tags": ["str"]
                    }}
                }}
                """
                response = self.model.generate_content(prompt)
                cleaned_text = response.text.replace("```json", "").replace("```", "")
                data = json.loads(cleaned_text)
                
                return TaskArtifact(**data)
            except Exception as e:
                print(f"LLM Error: {e}. Falling back to mock.")
        
        # Returning a mock TaskArtifact for structure demonstration (Fallback):
        return TaskArtifact(
            trip_id="DXB-20260110",
            itinerary_timeline=[
                {"event": "Flight Arrival", "time": parsed_data.arrival_time_utc}, 
                {"event": "Hotel Check-in", "time": parsed_data.check_in_time_utc}
            ],
            conflict_resolutions=[
                ConflictResolution(original_conflict="3-hour gap after flight arrival.", recommended_action="Draft email to hotel for early check-in.")
            ],
            packing_inputs=PackingInput(
                weather_summary="Hot and clear, high UV index.", 
                activities_tags=parsed_data.raw_activities,
                compliance_tags=["Visa Required", "Type C Power Adapter"]
            )
        )