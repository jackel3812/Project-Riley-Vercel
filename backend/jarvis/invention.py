import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_invention(prompt):
    """
    Generate an original invention concept based on the prompt
    """
    try:
        system_message = """
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
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in invention generation: {e}")
        return {
            "error": "Failed to generate invention",
            "details": str(e)
        }

def evaluate_invention(invention_concept):
    """
    Evaluate the feasibility and originality of an invention concept
    """
    try:
        system_message = """
        You are Riley, an advanced AI specialized in evaluating inventions.
        Analyze the provided invention concept and evaluate it on:
        1. Technical feasibility (1-10)
        2. Market potential (1-10)
        3. Originality (1-10)
        4. Implementation complexity (1-10, where 1 is most complex)
        5. Provide specific feedback on strengths and weaknesses
        
        Format the response as a structured JSON object with these ratings and feedback.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Evaluate this invention concept: {invention_concept}"}
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in invention evaluation: {e}")
        return {
            "error": "Failed to evaluate invention",
            "details": str(e)
        }
