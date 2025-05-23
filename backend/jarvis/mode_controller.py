import os
from .nlp_engine import generate_response

class ModeController:
    def __init__(self):
        """
        Initialize the mode controller with available modes and default mode
        """
        self.available_modes = [
            "genius",      # Highly intellectual and analytical
            "inventor",    # Creative and innovative
            "explorer",    # Curious and informative
            "scientist",   # Methodical and precise
            "engineer",    # Practical and solution-oriented
            "storyteller", # Narrative and engaging
            "assistant",   # Helpful and supportive
            "teacher"      # Educational and explanatory
        ]
        
        # Get default mode from environment or use "assistant"
        self.current_mode = os.getenv('RILEY_MODE', 'assistant')
        
        # Ensure current mode is valid
        if self.current_mode not in self.available_modes:
            self.current_mode = "assistant"
    
    def get_current_mode(self):
        """
        Get the current mode
        """
        return self.current_mode
    
    def switch_mode(self, new_mode):
        """
        Switch to a new mode if it's valid
        """
        if new_mode in self.available_modes:
            self.current_mode = new_mode
            return True
        return False
    
    def get_mode_description(self, mode=None):
        """
        Get a description of the specified mode or current mode
        """
        mode = mode or self.current_mode
        
        descriptions = {
            "genius": "Highly intellectual and analytical, focusing on deep insights and complex problem-solving.",
            "inventor": "Creative and innovative, specializing in generating novel ideas and solutions.",
            "explorer": "Curious and informative, focused on discovering and sharing knowledge.",
            "scientist": "Methodical and precise, emphasizing evidence-based reasoning and experimentation.",
            "engineer": "Practical and solution-oriented, focusing on implementation and optimization.",
            "storyteller": "Narrative and engaging, specializing in creative expression and communication.",
            "assistant": "Helpful and supportive, prioritizing user needs and practical assistance.",
            "teacher": "Educational and explanatory, focusing on clear instruction and knowledge transfer."
        }
        
        return descriptions.get(mode, "Unknown mode")
    
    def generate_response(self, text, mode=None):
        """
        Generate a response based on the specified mode or current mode
        """
        mode = mode or self.current_mode
        
        # Generate response using the NLP engine with mode-specific context
        system_prompt = f"You are Riley, an AI assistant operating in {mode} mode. {self.get_mode_description(mode)}"
        
        return generate_response(text, mode)
    
    def generate_joke(self, mode=None):
        """
        Generate a joke based on the specified mode or current mode
        """
        mode = mode or self.current_mode
        
        # Different joke styles based on mode
        joke_prompt = f"Tell a joke in the style of a {mode}."
        
        return generate_response(joke_prompt, mode)
