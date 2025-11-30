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