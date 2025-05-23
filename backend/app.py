from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import time
from werkzeug.middleware.proxy_fix import ProxyFix

# Import Riley modules
from jarvis.nlp_engine import process_input, generate_response
from jarvis.memory_engine import MemoryEngine
from jarvis.mode_controller import ModeController
from jarvis.invention import InventionEngine
from jarvis.equation_solver import EquationSolver
from jarvis.wiki_researcher import WikipediaSearch
from jarvis.github_learning import GitHubLearning
from jarvis.auto_repair import CodeAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('riley-api')

# Initialize Flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
CORS(app)

# Initialize Riley components
memory_engine = MemoryEngine()
mode_controller = ModeController()
invention_engine = InventionEngine()
equation_solver = EquationSolver()
wiki_researcher = WikipediaSearch()
github_learning = GitHubLearning()
code_analyzer = CodeAnalyzer()

# Get allowed tools from environment
allowed_tools = os.getenv('ALLOWED_TOOLS', '["invention", "web_search", "wiki"]')
try:
    ALLOWED_TOOLS = json.loads(allowed_tools)
except:
    ALLOWED_TOOLS = ["invention", "web_search", "wiki"]
    logger.warning(f"Failed to parse ALLOWED_TOOLS, using default: {ALLOWED_TOOLS}")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    })

# Main chat endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process a chat message and return a response
    
    Request body:
    {
        "user_id": "string",  // Unique identifier for the user
        "message": "string",  // The user's message
        "mode": "string",     // Optional: The mode to use (default: current mode)
        "context": []         // Optional: Previous conversation context
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        requested_mode = data.get('mode')
        context = data.get('context', [])
        
        # Log the request
        logger.info(f"Chat request from user {user_id}: {message[:50]}...")
        
        # Get current mode or use requested mode
        if requested_mode and mode_controller.switch_mode(requested_mode):
            current_mode = requested_mode
        else:
            current_mode = mode_controller.get_current_mode()
        
        # Process the input to determine intent
        intent, processed_text = process_input(message)
        
        # Generate response based on intent and mode
        response_text = mode_controller.generate_response(processed_text)
        
        # Store the interaction in memory
        memory_engine.store_interaction(
            user_id=user_id,
            query=message,
            response=response_text,
            intent=intent,
            mode=current_mode
        )
        
        # Return the response
        return jsonify({
            "response": response_text,
            "mode": current_mode,
            "intent": intent
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to process chat request",
            "details": str(e)
        }), 500

# Invention endpoint
@app.route('/api/invent', methods=['POST'])
def invent():
    """
    Generate an invention based on a prompt
    
    Request body:
    {
        "user_id": "string",     // Unique identifier for the user
        "prompt": "string",      // The invention prompt
        "field": "string",       // Optional: The field of invention (default: "general")
        "constraints": ["string"] // Optional: Constraints for the invention
    }
    """
    try:
        # Check if invention tool is allowed
        if "invention" not in ALLOWED_TOOLS:
            return jsonify({
                "error": "Invention tool is not allowed",
                "allowed_tools": ALLOWED_TOOLS
            }), 403
        
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        prompt = data.get('prompt', '')
        field = data.get('field', 'general')
        constraints = data.get('constraints', [])
        
        # Log the request
        logger.info(f"Invention request from user {user_id}: {prompt[:50]}...")
        
        # Generate invention
        invention = invention_engine.generate(prompt, field, constraints)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="invention",
            key=prompt,
            value=invention
        )
        
        return jsonify(invention)
    except Exception as e:
        logger.error(f"Error in invention endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to generate invention",
            "details": str(e)
        }), 500

# Equation solving endpoint
@app.route('/api/equation', methods=['POST'])
def solve_equation():
    """
    Solve an equation or mathematical problem
    
    Request body:
    {
        "user_id": "string",  // Unique identifier for the user
        "equation": "string", // The equation or problem to solve
        "format": "string"    // Optional: Output format (default: "text", options: "text", "latex", "steps")
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        equation = data.get('equation', '')
        output_format = data.get('format', 'text')
        
        # Log the request
        logger.info(f"Equation request from user {user_id}: {equation}")
        
        # Solve the equation
        solution = equation_solver.solve(equation, output_format)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="equation",
            key=equation,
            value=solution
        )
        
        return jsonify(solution)
    except Exception as e:
        logger.error(f"Error in equation endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to solve equation",
            "details": str(e)
        }), 500

# Wikipedia search endpoint
@app.route('/api/search', methods=['POST'])
def search():
    """
    Search Wikipedia for information
    
    Request body:
    {
        "user_id": "string", // Unique identifier for the user
        "query": "string"    // The search query
    }
    """
    try:
        # Check if web search tool is allowed
        if "web_search" not in ALLOWED_TOOLS and "wiki" not in ALLOWED_TOOLS:
            return jsonify({
                "error": "Web search tool is not allowed",
                "allowed_tools": ALLOWED_TOOLS
            }), 403
        
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        query = data.get('query', '')
        
        # Log the request
        logger.info(f"Search request from user {user_id}: {query}")
        
        # Search Wikipedia
        results = wiki_researcher.search(query)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="search",
            key=query,
            value=results
        )
        
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to search Wikipedia",
            "details": str(e)
        }), 500

# GitHub learning endpoint
@app.route('/api/github', methods=['POST'])
def github():
    """
    Analyze a GitHub repository
    
    Request body:
    {
        "user_id": "string",  // Unique identifier for the user
        "repo_url": "string"  // The GitHub repository URL
    }
    """
    try:
        # Check if GitHub tool is allowed
        if "github" not in ALLOWED_TOOLS:
            return jsonify({
                "error": "GitHub tool is not allowed",
                "allowed_tools": ALLOWED_TOOLS
            }), 403
        
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        repo_url = data.get('repo_url', '')
        
        # Log the request
        logger.info(f"GitHub analysis request from user {user_id}: {repo_url}")
        
        # Analyze GitHub repository
        analysis = github_learning.analyze_repo(repo_url)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="github",
            key=repo_url,
            value=analysis
        )
        
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Error in GitHub endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to analyze GitHub repository",
            "details": str(e)
        }), 500

# Code repair endpoint
@app.route('/api/repair', methods=['POST'])
def repair():
    """
    Analyze and repair code
    
    Request body:
    {
        "user_id": "string", // Unique identifier for the user
        "code": "string",    // The code to analyze and repair
        "language": "string" // Optional: The programming language
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        code = data.get('code', '')
        language = data.get('language')
        
        # Check if self-editing is allowed
        allow_self_editing = os.getenv('ALLOW_SELF_EDITING', 'false').lower() == 'true'
        if not allow_self_editing:
            return jsonify({
                "error": "Self-editing is not allowed",
                "details": "Set ALLOW_SELF_EDITING=true to enable this feature"
            }), 403
        
        # Log the request
        logger.info(f"Code repair request from user {user_id}")
        
        # Analyze and repair code
        repaired_code, changes = code_analyzer.analyze_and_repair(code, language)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="code_repair",
            key=code[:50],  # Use first 50 chars as key
            value={
                "original": code,
                "repaired": repaired_code,
                "changes": changes
            }
        )
        
        return jsonify({
            "repaired_code": repaired_code,
            "changes": changes
        })
    except Exception as e:
        logger.error(f"Error in repair endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to repair code",
            "details": str(e)
        }), 500

# Memory retrieval endpoint
@app.route('/api/memory', methods=['GET'])
def get_memory():
    """
    Retrieve memory items
    
    Query parameters:
    - user_id: Unique identifier for the user
    - type: Optional: Memory type (default: "all")
    - limit: Optional: Maximum number of items to return (default: 10)
    """
    try:
        user_id = request.args.get('user_id', 'anonymous')
        memory_type = request.args.get('type', 'all')
        limit = int(request.args.get('limit', 10))
        
        # Log the request
        logger.info(f"Memory retrieval request from user {user_id}, type: {memory_type}, limit: {limit}")
        
        # Retrieve memory
        memories = memory_engine.retrieve_memory(
            user_id=user_id,
            memory_type=memory_type,
            limit=limit
        )
        
        return jsonify(memories)
    except Exception as e:
        logger.error(f"Error in memory endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve memory",
            "details": str(e)
        }), 500

# User settings endpoint
@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """
    Get or update user settings
    
    GET query parameters:
    - user_id: Unique identifier for the user
    
    POST request body:
    {
        "user_id": "string",     // Unique identifier for the user
        "default_mode": "string", // Optional: Default mode
        "voice_enabled": boolean, // Optional: Whether voice is enabled
        "allow_self_editing": boolean, // Optional: Whether self-editing is allowed
        "allowed_tools": ["string"] // Optional: List of allowed tools
    }
    """
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id', 'anonymous')
            
            # Log the request
            logger.info(f"Settings retrieval request from user {user_id}")
            
            # Get user settings
            settings = memory_engine.get_user_settings(user_id)
            return jsonify(settings)
        
        elif request.method == 'POST':
            data = request.json
            user_id = data.get('user_id', 'anonymous')
            
            # Log the request
            logger.info(f"Settings update request from user {user_id}")
            
            # Update user settings
            updated_settings = memory_engine.update_user_settings(
                user_id=user_id,
                settings=data
            )
            return jsonify(updated_settings)
    except Exception as e:
        logger.error(f"Error in settings endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to process settings request",
            "details": str(e)
        }), 500

# Facts management endpoint
@app.route('/api/facts', methods=['GET', 'POST'])
def facts():
    """
    Get or store facts
    
    GET query parameters:
    - user_id: Unique identifier for the user
    - source: Optional: Fact source
    - limit: Optional: Maximum number of facts to return (default: 10)
    
    POST request body:
    {
        "user_id": "string",   // Unique identifier for the user
        "fact": "string",      // The fact to store
        "source": "string",    // Optional: Fact source (default: "user")
        "confidence": number   // Optional: Confidence level (default: 1.0)
    }
    """
    try:
        if request.method == 'GET':
            user_id = request.args.get('user_id', 'anonymous')
            source = request.args.get('source')
            limit = int(request.args.get('limit', 10))
            
            # Log the request
            logger.info(f"Facts retrieval request from user {user_id}, source: {source}, limit: {limit}")
            
            # Get facts
            facts = memory_engine.retrieve_facts(
                user_id=user_id,
                source=source,
                limit=limit
            )
            return jsonify(facts)
        
        elif request.method == 'POST':
            data = request.json
            user_id = data.get('user_id', 'anonymous')
            fact = data.get('fact')
            source = data.get('source', 'user')
            confidence = float(data.get('confidence', 1.0))
            
            # Log the request
            logger.info(f"Fact storage request from user {user_id}: {fact[:50]}...")
            
            # Store fact
            fact_id = memory_engine.store_fact(
                user_id=user_id,
                fact=fact,
                source=source,
                confidence=confidence
            )
            
            return jsonify({
                "status": "success",
                "fact_id": fact_id
            })
    except Exception as e:
        logger.error(f"Error in facts endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to process facts request",
            "details": str(e)
        }), 500

# Mode switching endpoint
@app.route('/api/mode-switch', methods=['POST'])
def mode_switch():
    """
    Switch the AI mode
    
    Request body:
    {
        "user_id": "string", // Unique identifier for the user
        "mode": "string"     // The mode to switch to
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        new_mode = data.get('mode')
        
        if not new_mode:
            return jsonify({
                "error": "Mode not specified",
                "available_modes": mode_controller.available_modes
            }), 400
        
        # Log the request
        logger.info(f"Mode switch request from user {user_id}: {new_mode}")
        
        # Switch mode
        success = mode_controller.switch_mode(new_mode)
        
        if success:
            # Store the mode change in memory
            memory_engine.store_memory(
                user_id=user_id,
                memory_type="mode_change",
                key=new_mode,
                value={
                    "previous_mode": mode_controller.get_current_mode(),
                    "new_mode": new_mode,
                    "timestamp": time.time()
                }
            )
            
            return jsonify({
                "status": "success",
                "mode": new_mode,
                "description": mode_controller.get_mode_description(new_mode)
            })
        else:
            return jsonify({
                "error": "Invalid mode",
                "available_modes": mode_controller.available_modes
            }), 400
    except Exception as e:
        logger.error(f"Error in mode-switch endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to switch mode",
            "details": str(e)
        }), 500

# Joke generation endpoint
@app.route('/api/joke', methods=['POST'])
def joke():
    """
    Generate a joke
    
    Request body:
    {
        "user_id": "string", // Unique identifier for the user
        "mode": "string"     // Optional: The mode to use for joke generation
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        joke_mode = data.get('mode')
        
        # Log the request
        logger.info(f"Joke request from user {user_id}, mode: {joke_mode}")
        
        # Generate joke
        joke_text = mode_controller.generate_joke(joke_mode)
        
        # Store in memory
        memory_engine.store_memory(
            user_id=user_id,
            memory_type="joke",
            key=f"joke_{time.time()}",
            value={
                "joke": joke_text,
                "mode": joke_mode or mode_controller.get_current_mode()
            }
        )
        
        return jsonify({
            "joke": joke_text,
            "mode": joke_mode or mode_controller.get_current_mode()
        })
    except Exception as e:
        logger.error(f"Error in joke endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to generate joke",
            "details": str(e)
        }), 500

# Voice processing endpoint
@app.route('/api/voice', methods=['POST'])
def voice():
    """
    Process voice input and return a response
    
    Request body:
    - audio: The audio file (multipart/form-data)
    - user_id: Unique identifier for the user
    - mode: Optional: The mode to use (default: current mode)
    
    Returns:
    - Audio response file
    """
    try:
        # Check if voice is enabled
        voice_enabled = os.getenv('VOICE_ENABLED', 'false').lower() == 'true'
        if not voice_enabled:
            return jsonify({
                "error": "Voice processing is not enabled",
                "details": "Set VOICE_ENABLED=true to enable this feature"
            }), 403
        
        user_id = request.form.get('user_id', 'anonymous')
        mode = request.form.get('mode')
        
        # Check if audio file is provided
        if 'audio' not in request.files:
            return jsonify({
                "error": "No audio file provided"
            }), 400
        
        audio_file = request.files['audio']
        
        # Log the request
        logger.info(f"Voice processing request from user {user_id}")
        
        # TODO: Implement voice processing
        # This would involve:
        # 1. Converting speech to text
        # 2. Processing the text with the chat endpoint
        # 3. Converting the response text to speech
        
        # For now, return a placeholder response
        return jsonify({
            "error": "Voice processing not implemented yet",
            "details": "This feature is coming soon"
        }), 501
    except Exception as e:
        logger.error(f"Error in voice endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to process voice input",
            "details": str(e)
        }), 500

# Stream response endpoint (for real-time chat)
@app.route('/api/stream', methods=['POST'])
def stream():
    """
    Stream a response for real-time chat
    
    Request body:
    {
        "user_id": "string",  // Unique identifier for the user
        "message": "string",  // The user's message
        "mode": "string"      // Optional: The mode to use (default: current mode)
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        requested_mode = data.get('mode')
        
        # Log the request
        logger.info(f"Stream request from user {user_id}: {message[:50]}...")
        
        # Get current mode or use requested mode
        if requested_mode and mode_controller.switch_mode(requested_mode):
            current_mode = requested_mode
        else:
            current_mode = mode_controller.get_current_mode()
        
        # Process the input to determine intent
        intent, processed_text = process_input(message)
        
        def generate():
            # This is a placeholder for actual streaming implementation
            # In a real implementation, you would use SSE or WebSockets
            yield json.dumps({"mode": current_mode, "intent": intent}) + "\n"
            
            # Simulate streaming by yielding chunks of the response
            response_text = mode_controller.generate_response(processed_text)
            words = response_text.split()
            
            for i in range(0, len(words), 3):
                chunk = " ".join(words[i:i+3])
                yield json.dumps({"chunk": chunk}) + "\n"
                time.sleep(0.1)  # Simulate delay
            
            # Store the interaction in memory after streaming is complete
            memory_engine.store_interaction(
                user_id=user_id,
                query=message,
                response=response_text,
                intent=intent,
                mode=current_mode
            )
            
            yield json.dumps({"done": True}) + "\n"
        
        return Response(generate(), mimetype='text/event-stream')
    except Exception as e:
        logger.error(f"Error in stream endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to stream response",
            "details": str(e)
        }), 500

# Run the app
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting Riley API on port {port}, debug={debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
