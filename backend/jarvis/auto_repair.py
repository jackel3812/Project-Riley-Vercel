import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def check_and_repair_code(code, language=None):
    """
    Check code for issues and repair it
    """
    try:
        # Detect language if not provided
        if not language:
            language = detect_language(code)
        
        # Check for issues
        issues = check_code_issues(code, language)
        
        # If no issues found, return the original code
        if not issues or len(issues) == 0:
            return code, []
        
        # Repair the code
        repaired_code = repair_code(code, issues, language)
        
        return repaired_code, issues
    except Exception as e:
        print(f"Error in code repair: {e}")
        return code, [{
            "error": "Failed to repair code",
            "details": str(e)
        }]

def detect_language(code):
    """
    Detect the programming language of the code
    """
    try:
        system_message = """
        You are Riley, an advanced AI specialized in code analysis.
        Detect the programming language of the provided code snippet.
        Return only the language name (e.g., "python", "javascript", "typescript", "java", etc.).
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": code}
            ]
        )
        
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Error detecting language: {e}")
        return "unknown"

def check_code_issues(code, language):
    """
    Check code for issues using OpenAI
    """
    try:
        system_message = f"""
        You are Riley, an advanced AI specialized in code analysis and repair.
        Analyze the provided {language} code and identify issues such as:
        1. Syntax errors
        2. Logical errors
        3. Performance issues
        4. Security vulnerabilities
        5. Style inconsistencies
        6. Best practice violations
        
        Format the response as a JSON array of issues, where each issue has:
        - "type": The type of issue (syntax, logical, performance, security, style, best_practice)
        - "line": The approximate line number (if applicable)
        - "description": A brief description of the issue
        - "severity": The severity level (low, medium, high)
        - "suggestion": A suggestion for fixing the issue
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": code}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("issues", [])
    except Exception as e:
        print(f"Error checking code issues: {e}")
        return []

def repair_code(code, issues, language):
    """
    Repair code based on identified issues
    """
    try:
        issues_json = json.dumps(issues)
        
        system_message = f"""
        You are Riley, an advanced AI specialized in code repair.
        Fix the provided {language} code based on the identified issues.
        Return the complete fixed code, not just the changes.
        Maintain the original functionality while addressing the issues.
        Add comments explaining significant changes.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Code:\n\n{code}\n\nIssues:\n{issues_json}"}
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error repairing code: {e}")
        return code
