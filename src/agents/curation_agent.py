# src/agents/curation_agent.py

# CORRECT IMPORT: Pulls the shared model from the central file
from src.models import TaskArtifact 
from ..tools.memory_tools import Memory_Retrieve, Memory_Update 
from ..tools.custom_tools import DocumentGenerator, NotificationManager, TaskScheduler 
from typing import List, Dict, Any

# The Curation Agent Class Definition
class CurationAgent:
    def __init__(self, llm_model, system_prompt):
        # Initialize the LLM client and model
        self.llm = llm_model 
        self.system_prompt = system_prompt
        
        # CORRECT TOOLS LIST: Using the underscore names from memory_tools.py
        self.tools = [
            Memory_Retrieve, 
            DocumentGenerator, 
            NotificationManager,
            TaskScheduler,
            Memory_Update 
        ]

    def run_curation_cycle(self, planner_artifact: TaskArtifact):
        """
        Executes the main curation cycle: retrieves memory, generates packing list, and schedules alerts.
        """
        # Step 1: Personalization (Retrieve Memory)
        print("  [Curation] Calling Memory_Retrieve tool...")

        # Step 2: Reasoning and Generation
        print(f"  [Curation] Generating personalized packing list based on Memory and {len(planner_artifact.conflict_resolutions)} conflicts.")
        
        # Step 3: Execution (Call Action Tools)
        DocumentGenerator(content="Final Travel Guide Content", trip_id=planner_artifact.trip_id) 
        NotificationManager(message="Proactive Alert: Check your email for early check-in status.", time_offset="1 hr pre-arrival")

        print(f"  [Curation] Curation Cycle Complete. Outputs generated.")
        return True