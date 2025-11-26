# src/agents/loop_monitor_agent.py

from src.models import MonitoringConfig, TriggerThreshold # Import from central models file
from ..tools.api_connectors import MonitorAPICheck 
import time

class AdaptationMonitor:
    def __init__(self, monitoring_config: MonitoringConfig):
        self.config = monitoring_config
        self.monitor_tool = MonitorAPICheck 

    def start_monitoring_loop(self):
        """
        Continuously monitors critical checkpoints and returns data if a critical 
        change is found, signaling main.py to re-initiate the Planner Agent.
        """
        print(f"\n--- Loop Agent Started for Trip {self.config.trip_id} ---")
        
        while True:
            critical_change_detected = False
            
            for checkpoint in self.config.critical_checkpoints:
                
                # Step 1: Execute the monitoring tool 
                current_status = self.monitor_tool(
                    check_type=checkpoint.check_type, 
                    location=checkpoint.location
                )
                
                # Step 2: Evaluate against the trigger threshold
                if current_status.is_critical(checkpoint.trigger_threshold):
                    critical_change_detected = True
                    print(f"!!! CRITICAL CHANGE: {current_status.raw_data.get('message')}. RE-PLANNING REQUIRED.")
                    
                    # Step 3: Trigger Re-Plan (Exit the loop and return the new data)
                    return current_status.raw_data 

            if not critical_change_detected:
                print(f"Monitoring check complete. Next check in {self.config.monitoring_interval_min} minutes.")
            
            # Wait for the next monitoring interval
            time.sleep(self.config.monitoring_interval_min * 60)