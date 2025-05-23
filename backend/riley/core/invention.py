import os
import json
from openai import OpenAI

class InventionEngine:
    def __init__(self):
        """
        Initialize the invention engine
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def generate(self, prompt, field="general", constraints=None):
        """
        Generate an invention based on the prompt, field, and constraints
        """
        try:
            if constraints is None:
                constraints = []
            
            # Create a system prompt for invention generation
            system_prompt = """
            You are Riley, an advanced AI specialized in invention generation. 
            Create a detailed, original invention concept based on the user's prompt.
            Include:
            1. A catchy name for the invention
            2. A concise description of what it does
            3. Key features and benefits
            4. Potential applications
            5. Basic technical implementation details
            6. Novelty aspects that make it unique
            
            Format the response as a structured JSON object with these sections.
            """
            
            # Add field-specific guidance
            if field != "general":
                system_prompt += f"\nFocus specifically on the field of {field}."
            
            # Add constraints
            if constraints:
                constraints_text = "\nConsider the following constraints:\n"
                for i, constraint in enumerate(constraints):
                    constraints_text += f"{i+1}. {constraint}\n"
                system_prompt += constraints_text
            
            # Use OpenAI to generate the invention
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            invention_json = json.loads(response.choices[0].message.content)
            
            # Add metadata
            invention_json["meta"] = {
                "prompt": prompt,
                "field": field,
                "constraints": constraints
            }
            
            return invention_json
        except Exception as e:
            print(f"Error in invention generation: {e}")
            return {
                "error": "Failed to generate invention",
                "details": str(e)
            }
    
    def evaluate(self, invention):
        """
        Evaluate an invention concept
        """
        try:
            # Create a system prompt for invention evaluation
            system_prompt = """
            You are Riley, an advanced AI specialized in evaluating inventions.
            Analyze the provided invention concept and evaluate it on:
            1. Technical feasibility (1-10)
            2. Market potential (1-10)
            3. Originality (1-10)
            4. Implementation complexity (1-10, where 1 is most complex)
            5. Provide specific feedback on strengths and weaknesses
            
            Format the response as a structured JSON object with these ratings and feedback.
            """
            
            # Convert invention to string if it's a dict
            if isinstance(invention, dict):
                invention_str = json.dumps(invention)
            else:
                invention_str = invention
            
            # Use OpenAI to evaluate the invention
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Evaluate this invention concept: {invention_str}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            evaluation = json.loads(response.choices[0].message.content)
            
            return evaluation
        except Exception as e:
            print(f"Error in invention evaluation: {e}")
            return {
                "error": "Failed to evaluate invention",
                "details": str(e)
            }
