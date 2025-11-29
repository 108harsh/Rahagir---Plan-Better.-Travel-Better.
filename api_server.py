# api_server.py

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from src.main import main # Import the main execution function
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Mount the 'public' directory to serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="public"), name="static")

# Serve the index.html at the root
@app.get("/")
async def read_index():
    return FileResponse('public/index.html')

@app.post("/plan_trip")
def plan_trip_endpoint(input_data: TravelInput):
    """
    Endpoint that triggers the full sequential Planner -> Curation agent workflow.
    """
    try:
        print(f"\n[API TRIGGERED] User {input_data.user_id} requesting plan for: {input_data.raw_user_input[:50]}...")
        
        # Call the actual main agent logic
        # We capture the result to return it to the frontend
        result = main(input_data.raw_user_input, input_data.user_id)
        
        return {
            "status": "Success",
            "message": result if isinstance(result, str) else "Trip planned successfully! Check your notifications.",
            "trip_id": "DXB-20260110" # This would be dynamic in a real app
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Deployment Note ---
# To run this locally: uvicorn api_server:app --reload