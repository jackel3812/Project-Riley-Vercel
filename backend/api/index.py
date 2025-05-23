from flask import Flask, request, jsonify, Response
import os
import sys
import json

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app
from app import app as flask_app

# This is the handler for Vercel serverless functions
def handler(request):
    """
    Handle requests for Vercel serverless functions
    """
    # Process the request with the Flask app
    with flask_app.request_context(request):
        return flask_app.full_dispatch_request()
