# chat_client.py (Run this in a NEW terminal session)

import requests
import json

# --- Replace with your actual ADK/SDK client setup ---
# NOTE: In a real system, an LLM would generate this JSON structure
def generate_structured_payload(natural_language_input: str, user_id: str):
    """
    Simulates the NLU Router using a smart function (or LLM call) 
    to convert conversational text into the required API payload.
    """
    print(f"\n[Router] Analyzing: '{natural_language_input[:30]}...'")
    
    # In a real scenario, the LLM determines the best raw_user_input string
    # for the Planner Agent to parse.
    
    return {
        "raw_user_input": natural_language_input,
        "user_id": user_id
    }

# --- Conversational Client Logic ---
def chat_with_rahagir():
    print("===============================================")
    print("🗣️ Rahagir Conversational Client Active")
    print("===============================================")
    
    API_URL = "http://127.0.0.1:8000/plan_trip"
    MY_USER_ID = "harsh_gupta_college_student_2025"
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Rahagir: Goodbye! Safe travels.")
            break
            
        # 1. NLU Router generates structured payload
        payload = generate_structured_payload(user_input, MY_USER_ID)
        
        # 2. Send request to the live Rahagir API backend
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
            
            # 3. Generate Conversational Response from Backend Status
            data = response.json()
            
            if data.get('status') == 'Success':
                print(f"\nRahagir: Got it! Your personalized guide has been sent to your email and the monitoring system is now active.")
                print(f"         (Trip ID: {data.get('trip_id')})")
            else:
                print(f"\nRahagir: Hmm, I ran into an issue. Details: {data.get('message')}")
                
        except requests.exceptions.ConnectionError:
            print("\n🚨 Rahagir: Error connecting to the API. Is the uvicorn server running?")
        except requests.exceptions.HTTPError as e:
            print(f"\n🚨 Rahagir: Backend returned an error. Status: {e.response.status_code}")

if __name__ == "__main__":
    chat_with_rahagir()