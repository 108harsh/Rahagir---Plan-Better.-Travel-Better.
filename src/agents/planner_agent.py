# src/agents/planner_agent.py

from src.models import TaskArtifact, ConflictResolution, PackingInput
from ..tools.custom_tools import ItineraryParserOutput, ItineraryParser
from typing import List, Dict, Any
import os
import google.generativeai as genai
import json

class PlannerAgent:
    def __init__(self, llm_model, system_prompt):
        self.llm = llm_model 
        self.system_prompt = system_prompt
        self.tools = ['ItineraryParser', 'WeatherAPICall', 'GoogleSearch'] 
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("PlannerAgent: Connected to Gemini API.")
        else:
            print("PlannerAgent: No API Key found. Using MOCK mode.")

    def run_planning_cycle(self, raw_user_input: str) -> TaskArtifact:
        print("--- Planner Agent: Running Planning Cycle ---")
        
        # 1. Parse Input
        parsed_data = ItineraryParser(raw_user_input)
        
        # 2. Check if it's a valid trip request
        if not parsed_data.valid_trip:
            print("PlannerAgent: Detected CHAT intent.")
            if self.api_key:
                try:
                    chat_prompt = f"You are Rahagir, a helpful travel agent. The user said: '{raw_user_input}'. Respond conversationally and ask where they would like to go."
                    response = self.model.generate_content(chat_prompt)
                    return TaskArtifact(
                        trip_id="CHAT",
                        chat_response=response.text,
                        itinerary_timeline=[],
                        conflict_resolutions=[],
                        packing_inputs=None
                    )
                except Exception as e:
                    print(f"Chat LLM Error: {e}")
            
            return TaskArtifact(
                trip_id="CHAT",
                chat_response="Hello! I'm Rahagir. Where are you planning to travel today?",
                itinerary_timeline=[],
                conflict_resolutions=[],
                packing_inputs=None
            )

        # 3. Valid Trip Request -> Plan it
        if self.api_key:
            try:
                # Real LLM Call
                prompt = f"""
                {self.system_prompt}
                
                User Input: {raw_user_input}
                Parsed Data: {parsed_data.json()}
                
                Identify potential conflicts and suggest resolutions.
                Provide packing tips based on the destination ({parsed_data.destination_iata}).
                Generate 2-3 follow-up questions to ask the user.
                
                Return the result ONLY as a JSON object matching the TaskArtifact structure:
                {{
                    "trip_id": "str",
                    "itinerary_timeline": [{{"event": "str", "time": "str"}}],
                    "conflict_resolutions": [{{"original_conflict": "str", "recommended_action": "str"}}],
                    "packing_inputs": {{
                        "weather_summary": "str",
                        "activities_tags": ["str"],
                        "compliance_tags": ["str"]
                    }},
                    "follow_up_questions": ["str"]
                }}
                """
                response = self.model.generate_content(prompt)
                cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(cleaned_text)
                
                return TaskArtifact(**data)
            except Exception as e:
                print(f"LLM Error: {e}. Falling back to mock.")
        
        # Fallback Mock (Only if API fails AND it was a valid trip request)
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
            ),
            follow_up_questions=["Do you need a vegetarian meal on the flight?", "Would you like to book a desert safari?"]
        )