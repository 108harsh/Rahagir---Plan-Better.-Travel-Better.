# src/tools/memory_tools.py

import json
from typing import Dict, Any, Optional

# Define the location of the Memory Bank file (in the data/ folder)
# IMPORTANT: Ensure you have a 'data/' folder and 'memory_bank.json' file
MEMORY_FILE = "data/memory_bank.json" 

# --- 1. Memory_Retrieve Tool (READ) ---
def Memory_Retrieve(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the complete structured user profile (LTM) from the memory bank file 
    for the Curation Agent to use for personalization.
    """
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
            # Find and return the user's specific memory profile
            return data.get(user_id)
    except FileNotFoundError:
        print(f"ERROR: Memory file not found at {MEMORY_FILE}")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format in {MEMORY_FILE}")
        return None

# --- 2. Memory_Update Tool (WRITE) ---
def Memory_Update(user_id: str, feedback_type: str, new_entry: Dict[str, Any]) -> bool:
    """
    Adds a new lesson learned (e.g., a past error or a new preference) to the LTM.
    This tool is called post-trip to allow the agent to learn.
    """
    try:
        with open(MEMORY_FILE, 'r+') as f:
            data = json.load(f)
            
            if user_id in data:
                profile = data[user_id]
                
                # Check if the field exists and is a list (like 'past_packing_errors')
                if feedback_type in profile and isinstance(profile[feedback_type], list):
                    profile[feedback_type].append(new_entry)
                # Check if the field exists and is an object (like 'medical_constraints')
                elif feedback_type in profile and isinstance(profile[feedback_type], dict):
                    profile[feedback_type].update(new_entry)
                # If field doesn't exist, create it (e.g., creating a new custom field)
                else:
                    profile[feedback_type] = new_entry
                
                # Write the updated data back to the file
                f.seek(0) # Go to the start of the file
                json.dump(data, f, indent=4)
                f.truncate() # Remove any remaining old content
                return True
            return False

    except Exception as e:
        print(f"ERROR updating memory: {e}")
        return False