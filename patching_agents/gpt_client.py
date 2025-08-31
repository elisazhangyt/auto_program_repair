import logging
import sys
import os
from openai import OpenAI

# Add the parent directory to the path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GPT_MODEL
from typing import List
import openai

class GPTClient:
    def __init__(self):
        self.api_key = None
    
    def initialize_agent(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt):
        client = OpenAI(api_key=self.api_key)
        
        response = client.chat.completions.create(model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}])
        
        return response

    def receive_response(self, response):
        content = response.choices[0].message.content if response and hasattr(response, 'choices') else None
            
        return content