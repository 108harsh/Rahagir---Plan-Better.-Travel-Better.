import json
import os
from typing import Dict, Any, List

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'memory.json')

def load_memory() -> Dict[str, Any]:
    if not os.path.exists(MEMORY_FILE):
        return {"users": {}}
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(data: Dict[str, Any]):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def Memory_Retrieve(user_id: str, query_key: str = None) -> str:
    """
    Retrieves user preferences or constraints from the Memory Bank.
    If query_key is provided, returns that specific section.
    """
    print(f"--- Tool: Memory_Retrieve for {user_id} ---")
    data = load_memory()
    user_data = data.get("users", {}).get(user_id, {})
    
    if not user_data:
        # Fallback to default user if specific user not found (for demo)
        user_data = data.get("users", {}).get("default_user", {})
        
    if query_key and query_key in user_data:
        return json.dumps(user_data[query_key])
    
    return json.dumps(user_data)

def Memory_Update(user_id: str, section: str, value: Any) -> str:
    """
    Updates a section of the user's memory (e.g., adding a past trip or preference).
    """
    print(f"--- Tool: Memory_Update for {user_id} ---")
    data = load_memory()
    
    if user_id not in data["users"]:
        data["users"][user_id] = {"preferences": {}, "past_trips": [], "constraints": []}
        
    if section == "past_trips":
        if "past_trips" not in data["users"][user_id]:
             data["users"][user_id]["past_trips"] = []
        data["users"][user_id]["past_trips"].append(value)
    else:
        data["users"][user_id][section] = value
        
    save_memory(data)
    return "Memory updated successfully."