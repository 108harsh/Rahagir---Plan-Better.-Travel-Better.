import os
from src.agents.conversation_agent import ConversationalAgent

# Mock API Key for testing logic flow (even if LLM call fails, we want to see it try)
if not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = "mock_key"

agent = ConversationalAgent()

print("--- TEST: Hello ---")
# Mock history and context
try:
    response = agent.run("Hello", [], "{}")
    print(f"Response Type: {response.response_type}")
    print(f"Content: {response.content}")
except Exception as e:
    print(f"Error: {e}")
