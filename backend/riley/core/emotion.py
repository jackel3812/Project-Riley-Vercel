import os
import json
from openai import OpenAI

class EmotionEngine:
    def __init__(self):
        """
        Initialize the emotion engine
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def detect_emotion(self, text):
        """
        Detect emotion in text
        """
        try:
            # Create a system prompt for emotion detection
            system_prompt = """
            You are Riley, an advanced AI specialized in emotion detection.
            Analyze the provided text and identify the emotional content.
            Return a JSON object with:
            1. primary_emotion: The main emotion detected (e.g., joy, sadness, anger, fear, surprise, etc.)
            2. intensity: A value from 1-10 indicating the intensity of the emotion
            3. secondary_emotions: An array of other emotions present, if any
            4. confidence: A value from 0-1 indicating your confidence in this analysis
            5. explanation: A brief explanation of why you detected these emotions
            """
            
            # Use OpenAI to detect emotion
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            emotion_data = json.loads(response.choices[0].message.content)
            
            return emotion_data
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return {
                "primary_emotion": "neutral",
                "intensity": 1,
                "secondary_emotions": [],
                "confidence": 0.5,
                "explanation": "Error in emotion detection"
            }
    
    def generate_response(self, emotion_data, mode="assistant"):
        """
        Generate an emotional response based on detected emotion and mode
        """
        try:
            # Skip if emotion data is incomplete
            if not emotion_data or "primary_emotion" not in emotion_data:
                return None
            
            primary_emotion = emotion_data["primary_emotion"]
            intensity = emotion_data.get("intensity", 5)
            
            # Adjust response based on mode
            if mode == "assistant" or mode == "teacher":
                # Supportive and helpful
                if primary_emotion in ["sadness", "fear", "anxiety"]:
                    return "empathetic"
                elif primary_emotion in ["anger", "frustration"]:
                    return "calming"
                elif primary_emotion in ["joy", "excitement"]:
                    return "enthusiastic"
                else:
                    return "neutral"
            elif mode == "genius" or mode == "scientist":
                # More analytical
                return "analytical"
            elif mode == "inventor" or mode == "explorer":
                # More enthusiastic
                return "enthusiastic"
            elif mode == "storyteller":
                # More expressive
                if primary_emotion in ["sadness", "fear"]:
                    return "comforting"
                elif primary_emotion in ["joy", "excitement"]:
                    return "joyful"
                else:
                    return "engaging"
            else:
                return "neutral"
        except Exception as e:
            print(f"Error in emotion response generation: {e}")
            return "neutral"
