# src/tools/memory_tools.py

import json
from typing import Dict, Any, Optional

# Define the location of the Memory Bank file (in the data/ folder)
MEMORY_FILE = "data/memory_bank.json"

# --- 1. Memory_Retrieve Tool ---
def Memory_Retrieve(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves the complete structured user profile (LTM) from the memory bank file.
    Args:
        user_id: The unique identifier for the user (e.g., "harsh_gupta_college_student_2025").
    Returns:
        The user's complete memory schema dictionary, or None if not found.
    """
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
            # In a full system, you would query a database here. 
            # Here, we just return the full schema for the Curation Agent to use.
            return data.get(user_id)
    except FileNotFoundError:
        print(f"ERROR: Memory file not found at {MEMORY_FILE}")
        return None

# --- 2. Memory_Update Tool ---
def Memory_Update(user_id: str, feedback_type: str, new_entry: Dict[str, Any]) -> bool:
    """
    Adds a new lesson learned (e.g., a past error or a new preference) to the LTM.
    This tool is called at the end of a trip or after user feedback.
    """
    try:
        with open(MEMORY_FILE, 'r+') as f:
            data = json.load(f)
            
            if user_id in data:
                # Find the correct list (e.g., 'past_packing_errors') and append the new entry
                if feedback_type in data[user_id] and isinstance(data[user_id][feedback_type], list):
                    data[user_id][feedback_type].append(new_entry)
                elif feedback_type in data[user_id]:
                    # Handle updating dictionary fields
                    data[user_id][feedback_type].update(new_entry)
                
                # Write the updated data back to the file
                f.seek(0) # Go to the start of the file
                json.dump(data, f, indent=4)
                f.truncate() # Remove any remaining old content
                return True
            return False

    except Exception as e:
        print(f"ERROR updating memory: {e}")
        return False