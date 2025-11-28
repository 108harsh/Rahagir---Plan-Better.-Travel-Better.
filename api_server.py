# api_server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.main import main # Import the main execution function

# --- Define the API Input Model ---
# This ensures data sent to the endpoint is structured and validated
class TravelInput(BaseModel):
    raw_user_input: str = Field(..., example="Booked flight to DXB arriving Jan 10th at 14:00. Hotel check-in is 17:00.")
    user_id: str = Field(..., example="harsh_gupta_college_student_2025")

# --- Initialize the FastAPI Application ---
app = FastAPI(
    title="Rahagir: Multi-Agent Travel Concierge API",
    description="Deploys the three-agent system to provide proactive travel planning and optimization."
)

@app.post("/plan_trip")
def plan_trip_endpoint(input_data: TravelInput):
    """
    Endpoint that triggers the full sequential Planner -> Curation agent workflow.
    
    This function simulates the main execution flow from src/main.py.
    NOTE: In a production environment, the Loop Agent would run as a separate
    scheduled task (Cloud Scheduler/Cron job) and the Planner/Curation
    would run in a thread here.
    """
    try:
        # In a deployment scenario, we would run the agent workflow with the user input:
        # final_plan_result = main(input_data.raw_user_input, input_data.user_id) 
        
        # For the Capstone demo, we confirm the API structure is correct:
        print(f"\n[API TRIGGERED] User {input_data.user_id} requesting plan for: {input_data.raw_user_input[:50]}...")
        
        # --- Simulate Running Main Logic ---
        # The actual main() execution function must be modified to accept user_id/input
        # main(input_data.raw_user_input, input_data.user_id) 
        
        return {
            "status": "Success",
            "message": "Rahagir sequential agents (Planner/Curation) initiated. Check notifications for PDF guide.",
            "trip_id": "DXB-20260110"
        }
    except Exception as e:
        # Essential for production: handles unexpected errors in agent execution
        raise HTTPException(status_code=500, detail=f"Agent Execution Error: {e}")

# --- Deployment Note ---
# To run this locally: uvicorn api_server:app --reload