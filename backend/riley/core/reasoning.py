import os
import json
from openai import OpenAI

class ReasoningEngine:
    def __init__(self):
        """
        Initialize the reasoning engine
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
        
        # Mode descriptions
        self.mode_descriptions = {
            "assistant": "You are Riley, a helpful and friendly AI assistant.",
            "genius": "You are Riley, a brilliant AI with exceptional analytical abilities. Provide deep, insightful analysis.",
            "inventor": "You are Riley, an innovative AI focused on generating novel ideas and inventions. Think outside the box.",
            "explorer": "You are Riley, a curious AI that loves to discover and share knowledge about the world.",
            "scientist": "You are Riley, a methodical AI that approaches problems with scientific rigor and precision.",
            "engineer": "You are Riley, a practical AI focused on building and optimizing solutions to problems.",
            "storyteller": "You are Riley, a creative AI that excels at crafting engaging narratives and explanations.",
            "teacher": "You are Riley, an educational AI that explains complex concepts clearly and patiently."
        }
    
    def process(self, message, mode="assistant", user_id=None):
        """
        Process a message using the reasoning engine
        """
        try:
            # Get the system prompt for the current mode
            system_prompt = self.mode_descriptions.get(mode, self.mode_descriptions["assistant"])
            
            # Add command detection to the system prompt
            system_prompt += "\nDetect if the user is using a command like !idea, !analyze, !explain, !invent, !emotion, or !simulate and respond accordingly."
            
            # Check for commands in the message
            command = None
            if message.startswith("!"):
                command_parts = message.split(" ", 1)
                command = command_parts[0][1:]  # Remove the ! prefix
                if len(command_parts) > 1:
                    message = command_parts[1]
            
            # Modify the system prompt based on the command
            if command:
                if command == "idea" or command == "invent":
                    system_prompt = self.mode_descriptions["inventor"]
                elif command == "analyze":
                    system_prompt = self.mode_descriptions["genius"]
                elif command == "explain":
                    system_prompt = self.mode_descriptions["teacher"]
                elif command == "emotion":
                    system_prompt += "\nFocus on the emotional aspects of the user's message and respond with empathy."
                elif command == "simulate":
                    system_prompt += "\nSimulate the scenario described by the user in detail."
            
            # Use OpenAI to process the message
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            # Determine the intent (this would be more sophisticated in a real implementation)
            intent = command if command else "general"
            
            return {
                "text": response_text,
                "intent": intent,
                "mode": mode
            }
        except Exception as e:
            print(f"Error in reasoning engine: {e}")
            return {
                "text": "I'm having trouble processing that right now. Could you try again?",
                "intent": "error",
                "mode": mode
            }
