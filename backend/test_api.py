import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the API
BASE_URL = "http://localhost:5000"

# Test user ID
TEST_USER_ID = "test_user_123"

def test_health():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/api/health")
    print("Health Check:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_chat():
    """Test the chat endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "message": "Hello, Riley! Tell me about yourself.",
        "mode": "assistant"
    }
    response = requests.post(f"{BASE_URL}/api/chat", json=data)
    print("Chat:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_invention():
    """Test the invention endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "prompt": "A device that helps people stay focused while working",
        "field": "productivity",
        "constraints": ["must be affordable", "must be portable"]
    }
    response = requests.post(f"{BASE_URL}/api/invent", json=data)
    print("Invention:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_equation():
    """Test the equation endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "equation": "x^2 + 5x + 6 = 0",
        "format": "steps"
    }
    response = requests.post(f"{BASE_URL}/api/equation", json=data)
    print("Equation:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_search():
    """Test the search endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "query": "artificial intelligence"
    }
    response = requests.post(f"{BASE_URL}/api/search", json=data)
    print("Search:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_mode_switch():
    """Test the mode switch endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "mode": "inventor"
    }
    response = requests.post(f"{BASE_URL}/api/mode-switch", json=data)
    print("Mode Switch:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_joke():
    """Test the joke endpoint"""
    data = {
        "user_id": TEST_USER_ID,
        "mode": "storyteller"
    }
    response = requests.post(f"{BASE_URL}/api/joke", json=data)
    print("Joke:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def test_settings():
    """Test the settings endpoints"""
    # Get settings
    response = requests.get(f"{BASE_URL}/api/settings?user_id={TEST_USER_ID}")
    print("Get Settings:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()
    
    # Update settings
    data = {
        "user_id": TEST_USER_ID,
        "default_mode": "explorer",
        "voice_enabled": True,
        "allowed_tools": ["invention", "web_search", "wiki"]
    }
    response = requests.post(f"{BASE_URL}/api/settings", json=data)
    print("Update Settings:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    print()

def run_tests():
    """Run all tests"""
    print("=== Testing Riley AI API ===")
    test_health()
    test_chat()
    test_invention()
    test_equation()
    test_search()
    test_mode_switch()
    test_joke()
    test_settings()
    print("=== Tests Complete ===")

if __name__ == "__main__":
    run_tests()
