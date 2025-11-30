# src/main.py

from src.agents.planner_agent import PlannerAgent, TaskArtifact
from src.agents.curation_agent import CurationAgent
from src.agents.loop_monitor_agent import AdaptationMonitor, MonitoringConfig
from src.tools.custom_tools import ItineraryParser 
from src.tools.memory_tools import Memory_Retrieve, Memory_Update
from src.tools.doc_tools import DocumentGenerator
import json

# --- MOCKING: ADK Initialization ---
class ADKClient:
    def __init__(self):
        # print("ADK: Initializing Google ADK Client...")
        pass
    
    def process_task(self, agent_instance, task_input):
        return agent_instance.run_planning_cycle(task_input)

def load_config():
    return MonitoringConfig(
        trip_id="DXB-20260110",
        monitoring_interval_min=30,
        critical_checkpoints=[
            {"check_type": "Flight_Status", "location": "DXB", "trigger_threshold": {"delay_minutes": 60}},
        ]
    )

def main(raw_trip_input: str, user_id: str):
    """
    Main entry point for the conversational agent.
    """
    adk_client = ADKClient()
    config = load_config()
    
    # 1. Retrieve Context from Memory
    user_prefs = Memory_Retrieve(user_id)
    print(f"Loaded Context for {user_id}: {user_prefs}")

    # 2. Initialize Agents
    planner_prompt = f"You are Rahagir. User Context: {user_prefs}. Plan conflicts and packing."
    planner = PlannerAgent(adk_client, planner_prompt)
    
    # 3. Planner Execution
    print("\n[1] START: Planner Agent")
    final_artifact = planner.run_planning_cycle(raw_trip_input)
    
    # --- CHECK FOR CHAT RESPONSE ---
    if final_artifact.chat_response:
        return final_artifact.chat_response

    # 4. Curation Execution (Document Generation)
    print("\n[2] START: Curation Agent (Doc Gen)")
    doc_link = DocumentGenerator(final_artifact)
    
    # 5. Update Memory (Mock update for now)
    Memory_Update(user_id, "last_trip_id", final_artifact.trip_id)

    # 6. Construct Response
    questions_text = "\n".join([f"- {q}" for q in final_artifact.follow_up_questions])
    
    summary = (
        f"I've planned your trip to **{final_artifact.trip_id}**!\n\n"
        f"**Itinerary**:\n" + 
        "\n".join([f"- {item['time']}: {item['event']}" for item in final_artifact.itinerary_timeline]) +
        f"\n\n**Conflict Resolved**: {final_artifact.conflict_resolutions[0].recommended_action if final_artifact.conflict_resolutions else 'None'}\n\n"
        f"**Packing Tips**: {final_artifact.packing_inputs.weather_summary}\n"
        f"**Download Guide**: [Click here to download your PDF/Guide]({doc_link})\n\n"
        f"**Suggestions & Questions**:\n{questions_text}\n\n"
        f"I've also set up a monitor to check for flight delays every 30 mins."
    )
    return summary

if __name__ == "__main__":
    print(main("Test trip to London", "test_user"))