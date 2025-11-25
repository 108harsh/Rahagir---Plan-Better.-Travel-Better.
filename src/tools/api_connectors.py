# src/tools/api_connectors.py (NEW FILE)

from typing import Dict, Any

# Define a simple Status class to reflect current conditions
class CurrentStatus:
    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data
        
    def is_critical(self, threshold: TriggerThreshold) -> bool:
        """Logic to check if current status crosses the set threshold."""
        
        if self.raw_data.get('type') == 'Flight' and self.raw_data.get('delay') > threshold.delay_minutes:
            return True
        
        if self.raw_data.get('type') == 'Weather' and self.raw_data.get('alert') == threshold.weather_severity:
            return True
            
        return False

def MonitorAPICheck(check_type: str, location: str) -> CurrentStatus:
    """
    Mock function to simulate polling a Flight or Weather API for volatile data.
    """
    print(f"--- Tool: MonitorAPICheck checking {check_type} at {location} ---")
    
    # Return a status that is NOT critical by default
    return CurrentStatus(raw_data={'type': 'Flight', 'delay': 15, 'message': 'On Time'})