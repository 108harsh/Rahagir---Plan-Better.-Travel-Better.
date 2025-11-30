# src/agents/conversation_agent.py

import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json

class ConversationResponse(BaseModel):
    response_type: str = Field(..., description="Type of response: 'CHAT' or 'PLAN_REQUEST'")
    content: str = Field(..., description="The chat response content or the planning request details.")
    updated_memory: Optional[Dict[str, Any]] = Field(None, description="Updates to user memory based on the conversation.")

class ConversationalAgent:
    def __init__(self, system_prompt: str = ""):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.system_prompt = system_prompt
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            print("ConversationalAgent: No API Key found. Chat will be limited.")

    def run(self, user_input: str, history: List[Dict[str, str]], user_context: str) -> ConversationResponse:
        print("--- Conversational Agent: Processing Input ---")
        
        if not self.api_key:
            return ConversationResponse(
                response_type="CHAT",
                content="I'm running in offline mode. I can't chat freely, but I can try to plan a trip if you ask explicitly."
            )

        # Format history
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-10:]]) # Last 10 turns

        prompt = f"""
        You are Rahagir, an intelligent and friendly AI travel concierge.
        
        User Context: {user_context}
        
        Conversation History:
        {history_text}
        
        Current User Input: "{user_input}"
        
        Your Goal:
        1. Analyze the user's input.
        2. Determine if the user is asking to PLAN a specific trip (e.g., "Plan a trip to Paris", "I want to go to London next week").
        3. Determine if the user is just CHATTING, asking general questions, or modifying preferences (e.g., "Hello", "I like beaches", "What is the weather in Dubai?").
        
        Output Format (JSON ONLY):
        {{
            "response_type": "CHAT" or "PLAN_REQUEST",
            "content": "Your conversational response here (if CHAT) OR the raw input string (if PLAN_REQUEST)",
            "memory_update": {{ "key": "value" }} (Optional: if the user mentioned a preference like 'I like hiking', extract it here. Otherwise null.)
        }}
        
        Rules:
        - If the user says "Hello" or introduces themselves, just CHAT.
        - If the user asks a general question (e.g. "Where is good for hiking?"), answer it as CHAT.
        - ONLY use "PLAN_REQUEST" if the user explicitly asks to generate a full itinerary or plan.
        - Be helpful, witty, and professional.
        """
        
        try:
            response = self.model.generate_content(prompt)
            cleaned = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            
            return ConversationResponse(
                response_type=data.get("response_type", "CHAT"),
                content=data.get("content", ""),
                updated_memory=data.get("memory_update")
            )
        except Exception as e:
            print(f"Conversation Agent Error: {e}")
            return ConversationResponse(
                response_type="CHAT",
                content="I'm having a bit of trouble understanding. Could you say that again?"
            )
