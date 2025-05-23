# Riley AI API Documentation

This document provides information about the Riley AI API endpoints and how to use them.

## Base URL

In development: `http://localhost:5000`
In production: `https://your-deployment-url.vercel.app`

## Authentication

Currently, the API uses a simple user_id parameter for identification. More robust authentication will be added in future versions.

## Endpoints

### Health Check

\`\`\`
GET /api/health
\`\`\`

Check if the API is running.

**Response:**
\`\`\`json
{
  "status": "healthy",
  "timestamp": 1621234567.89,
  "version": "1.0.0"
}
\`\`\`

### Chat

\`\`\`
POST /api/chat
\`\`\`

Process a chat message and return a response.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "message": "string",
  "mode": "string",
  "context": []
}
\`\`\`

**Response:**
\`\`\`json
{
  "response": "string",
  "mode": "string",
  "intent": "string"
}
\`\`\`

### Invention

\`\`\`
POST /api/invent
\`\`\`

Generate an invention based on a prompt.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "prompt": "string",
  "field": "string",
  "constraints": ["string"]
}
\`\`\`

**Response:**
\`\`\`json
{
  "name": "string",
  "description": "string",
  "features": ["string"],
  "applications": ["string"],
  "technical_details": "string",
  "novelty": "string",
  "meta": {
    "prompt": "string",
    "field": "string",
    "constraints": ["string"]
  }
}
\`\`\`

### Equation Solving

\`\`\`
POST /api/equation
\`\`\`

Solve an equation or mathematical problem.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "equation": "string",
  "format": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "equation": "string",
  "solution": "string",
  "method": "string",
  "steps": ["string"],
  "latex": "string"
}
\`\`\`

### Wikipedia Search

\`\`\`
POST /api/search
\`\`\`

Search Wikipedia for information.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "query": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "query": "string",
  "title": "string",
  "summary": "string",
  "source": "string",
  "search_results": [
    {
      "title": "string",
      "snippet": "string",
      "pageid": "number"
    }
  ]
}
\`\`\`

### GitHub Analysis

\`\`\`
POST /api/github
\`\`\`

Analyze a GitHub repository.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "repo_url": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "repo_url": "string",
  "structure": {
    "file_count": "number",
    "file_types": {},
    "directory_structure": {}
  },
  "patterns": {},
  "insights": {}
}
\`\`\`

### Code Repair

\`\`\`
POST /api/repair
\`\`\`

Analyze and repair code.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "code": "string",
  "language": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "repaired_code": "string",
  "changes": [
    {
      "type": "string",
      "line": "number",
      "description": "string",
      "severity": "string",
      "suggestion": "string"
    }
  ]
}
\`\`\`

### Memory Retrieval

\`\`\`
GET /api/memory?user_id=string&type=string&limit=number
\`\`\`

Retrieve memory items.

**Response:**
\`\`\`json
[
  {
    "id": "number",
    "user_id": "string",
    "type": "string",
    "key": "string",
    "value": {},
    "timestamp": "string"
  }
]
\`\`\`

### User Settings

\`\`\`
GET /api/settings?user_id=string
\`\`\`

Get user settings.

**Response:**
\`\`\`json
{
  "user_id": "string",
  "default_mode": "string",
  "voice_enabled": "boolean",
  "allow_self_editing": "boolean",
  "allowed_tools": ["string"]
}
\`\`\`

\`\`\`
POST /api/settings
\`\`\`

Update user settings.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "default_mode": "string",
  "voice_enabled": "boolean",
  "allow_self_editing": "boolean",
  "allowed_tools": ["string"]
}
\`\`\`

**Response:**
\`\`\`json
{
  "user_id": "string",
  "default_mode": "string",
  "voice_enabled": "boolean",
  "allow_self_editing": "boolean",
  "allowed_tools": ["string"]
}
\`\`\`

### Facts Management

\`\`\`
GET /api/facts?user_id=string&source=string&limit=number
\`\`\`

Get facts.

**Response:**
\`\`\`json
[
  {
    "id": "number",
    "user_id": "string",
    "fact": "string",
    "source": "string",
    "confidence": "number",
    "timestamp": "string"
  }
]
\`\`\`

\`\`\`
POST /api/facts
\`\`\`

Store a fact.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "fact": "string",
  "source": "string",
  "confidence": "number"
}
\`\`\`

**Response:**
\`\`\`json
{
  "status": "success",
  "fact_id": "number"
}
\`\`\`

### Mode Switching

\`\`\`
POST /api/mode-switch
\`\`\`

Switch the AI mode.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "mode": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "status": "success",
  "mode": "string",
  "description": "string"
}
\`\`\`

### Joke Generation

\`\`\`
POST /api/joke
\`\`\`

Generate a joke.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "mode": "string"
}
\`\`\`

**Response:**
\`\`\`json
{
  "joke": "string",
  "mode": "string"
}
\`\`\`

### Voice Processing

\`\`\`
POST /api/voice
\`\`\`

Process voice input and return a response.

**Request Body:**
- Form data with audio file and user_id

**Response:**
- Audio file or error message

### Stream Response

\`\`\`
POST /api/stream
\`\`\`

Stream a response for real-time chat.

**Request Body:**
\`\`\`json
{
  "user_id": "string",
  "message": "string",
  "mode": "string"
}
\`\`\`

**Response:**
- Server-sent events stream with JSON chunks

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in case of failure.

Example error response:
\`\`\`json
{
  "error": "Error message",
  "details": "Detailed error information"
}
\`\`\`

## Environment Variables

The API requires the following environment variables:

- `OPENAI_API_KEY`: OpenAI API key
- `DATABASE_URL`: Database connection URL
- `RILEY_MODE`: Default mode (genius, inventor, explorer, etc.)
- `VOICE_ENABLED`: Whether voice processing is enabled
- `ALLOW_SELF_EDITING`: Whether self-editing is allowed
- `ALLOWED_TOOLS`: JSON array of allowed tools
\`\`\`

Let's create a simple test script to verify the API endpoints:
