# src/main.py

# Placeholder imports assuming ADK modules and Pydantic models are available
from src.agents.planner_agent import PlannerAgent, TaskArtifact
from src.agents.curation_agent import CurationAgent
from src.agents.loop_monitor_agent import AdaptationMonitor, MonitoringConfig
from src.tools.custom_tools import ItineraryParser # Example tool access

# --- MOCKING: ADK Initialization ---
# In a real ADK environment, this handles API keys, model loading, and context.
class ADKClient:
    def __init__(self):
        print("ADK: Initializing Google ADK Client...")
    
    def process_task(self, agent_instance, task_input):
        # Simulates the ADK running the agent's LLM core and tool-calling
        return agent_instance.run_planning_cycle(task_input)

# --- 1. Define Mock Configuration ---
# In a real ADK project, this data would be loaded from a config/YAML file.
def load_config():
    # Load Monitoring Configuration for the Loop Agent
    config = MonitoringConfig(
        trip_id="DXB-20260110",
        monitoring_interval_min=30,
        critical_checkpoints=[
            {"check_type": "Flight_Status", "location": "DXB", "trigger_threshold": {"delay_minutes": 60}},
        ]
    )
    return config

def main():
    # --- STEP A: Initialize the Environment and Input ---
    adk_client = ADKClient()
    config = load_config()
    raw_trip_input = "Booked flight to Dubai (DXB) arriving Jan 10th at 14:00. Hotel check-in is 17:00. I need my laptop for work."
    
    # Define Agent System Prompts (Loaded by ADK)
    planner_prompt = "You are the Rahagir Planner Agent, expert in conflict resolution."
    curation_prompt = "You are the Rahagir Curation Agent, focused on personalization and execution."

    # --- STEP B: Initialize Agents (ADK Style) ---
    planner = PlannerAgent(adk_client, planner_prompt)
    curator = CurationAgent(adk_client, curation_prompt)
    
    # --- STEP C: Execute Sequential Workflow (Planner -> Curation) ---
    print("\n[1] START: Planner Agent Execution (Parsing & Conflict Resolution)")
    
    # 1. Planner Agent runs (calls ItineraryParser, resolves time gap conflict)
    # The ADK runs the planner, enforcing the TaskArtifact structure.
    # final_artifact = adk_client.process_task(planner, raw_trip_input) 
    
    # --- MOCKING: Use a mock artifact to test the flow ---
    # src/main.py (Around line 54)

    # --- MOCKING: Use a mock artifact to test the flow ---
    final_artifact = TaskArtifact(
        trip_id=config.trip_id,
        itinerary_timeline=[], # Simplified for this demo
        conflict_resolutions=[{"original_conflict": "3-hour check-in gap.", "recommended_action": "Draft email for early check-in."}],
        packing_inputs={
            "weather_summary": "Hot", 
            "activities_tags": ["Business"],
            # --- ADDING THE MISSING FIELD ---
            "compliance_tags": ["Visa Required", "Type G Adapter"] 
        }
    )

    print("\n[2] TRANSITION (A2A Handoff): Planner -> Curation")
    print(f"Conflict Resolution Proposed: {final_artifact.conflict_resolutions[0].recommended_action}")

    # 2. Curation Agent runs (calls Memory_Retrieve, generates PDF, schedules alerts)
    print("\n[3] EXECUTE: Curation Agent (Personalization & Action Tools)")
    # adk_client.process_task(curator, final_artifact) 
    print("Curation Agent successfully called DocumentGenerator and NotificationManager.")

    # --- STEP D: Initiate Dynamic Adaptation (Loop Agent) ---
    print("\n[4] START: Adaptation Monitor (Loop Agent Initiation)")
    monitor = AdaptationMonitor(config)
    
    # The monitor is started in a non-blocking thread to check volatile data
    # critical_data = monitor.start_monitoring_loop() 
    
    print(f"Monitor running in background, checking every {config.monitoring_interval_min} minutes.")
    print("If critical data found, system will RE-INITIATE PLANNER AGENT.")
    
    # This architecture perfectly maps the diagram showing data flowing from sources 
    # through processing systems (Planner/Curation) and then constantly re-evaluated 
    # by the Loop Agent. 




if __name__ == "__main__":
    main()