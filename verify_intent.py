from dotenv import load_dotenv
load_dotenv()
from src.main import main

print("--- TEST 1: CHAT (Should be conversational) ---")
try:
    print(main("Hello there", "test_user"))
except Exception as e:
    print(f"TEST 1 FAILED: {e}")

print("\n--- TEST 2: PLAN (Should be a trip plan) ---")
try:
    print(main("Plan a 3-day trip to Lucknow starting Dec 1st", "test_user"))
except Exception as e:
    print(f"TEST 2 FAILED: {e}")
