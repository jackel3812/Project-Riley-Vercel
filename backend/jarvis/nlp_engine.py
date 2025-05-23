import os
from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def process_input(text):
    """
    Process user input to determine intent and extract key information
    """
    try:
        # Use OpenAI to analyze the input
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Riley, an advanced AI assistant. Analyze the user input and determine the intent and key information. Return a JSON with 'intent' and 'processed_text' fields."},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        result = json.loads(response.choices[0].message.content)
        intent = result.get('intent', 'general')
        processed_text = result.get('processed_text', text)
        
        return intent, processed_text
    except Exception as e:
        print(f"Error in NLP processing: {e}")
        return "general", text

def generate_response(text, mode="general"):
    """
    Generate a response based on the input text and current mode
    """
    try:
        # Use OpenAI to generate a response
        system_prompt = f"You are Riley, an advanced AI assistant operating in {mode} mode. Respond to the user's input accordingly."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in response generation: {e}")
        return "I'm having trouble processing that right now. Could you try again?"
