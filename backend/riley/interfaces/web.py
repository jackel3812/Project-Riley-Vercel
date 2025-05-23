def format_response(text, emotion=None, mode=None):
    """
    Format a response for the web interface
    """
    response = {
        "text": text,
        "emotion": emotion,
        "mode": mode
    }
    
    # Add emotion-specific formatting
    if emotion:
        if emotion == "empathetic":
            response["style"] = "empathetic"
        elif emotion == "calming":
            response["style"] = "calming"
        elif emotion == "enthusiastic":
            response["style"] = "enthusiastic"
        elif emotion == "analytical":
            response["style"] = "analytical"
        elif emotion == "comforting":
            response["style"] = "comforting"
        elif emotion == "joyful":
            response["style"] = "joyful"
        elif emotion == "engaging":
            response["style"] = "engaging"
        else:
            response["style"] = "neutral"
    else:
        response["style"] = "neutral"
    
    return response
