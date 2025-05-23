import os
import json
import re
from openai import OpenAI

class CodeAnalyzer:
    def __init__(self):
        """
        Initialize the code analyzer
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def analyze_and_repair(self, code):
        """
        Analyze and repair code
        """
        try:
            # Detect language
            language = self._detect_language(code)
            
            # Analyze code for issues
            issues = self._analyze_code(code, language)
            
            # If no issues found, return the original code
            if not issues or len(issues) == 0:
                return code, []
            
            # Repair the code
            repaired_code = self._repair_code(code, issues, language)
            
            return repaired_code, issues
        except Exception as e:
            print(f"Error in code analysis: {e}")
            return code, [{
                "type": "error",
                "description": f"Error analyzing code: {str(e)}",
                "severity": "high"
            }]
    
    def _detect_language(self, code):
        """
        Detect the programming language of the code
        """
        try:
            # Create a system prompt for language detection
            system_prompt = """
            You are Riley, an advanced AI specialized in code analysis.
            Detect the programming language of the provided code snippet.
            Return only the language name (e.g., "python", "javascript", "typescript", "java", etc.).
            """
            
            # Use OpenAI to detect language
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": code}
                ]
            )
            
            # Extract the language
            language = response.choices[0].message.content.strip().lower()
            
            return language
        except Exception as e:
            print(f"Error detecting language: {e}")
            return "unknown"
    
    def _analyze_code(self, code, language):
        """
        Analyze code for issues
        """
        try:
            # Create a system prompt for code analysis
            system_prompt = f"""
            You are Riley, an advanced AI specialized in code analysis.
            Analyze the provided {language} code and identify issues such as:
            1. Syntax errors
            2. Logical errors
            3. Performance issues
            4. Security vulnerabilities
            5. Style inconsistencies
            6. Best practice violations
            
            Format the response as a JSON object with an "issues" array, where each issue has:
            - "type": The type of issue (syntax, logical, performance, security, style, best_practice)
            - "line": The approximate line number (if applicable)
            - "description": A brief description of the issue
            - "severity": The severity level (low, medium, high)
            - "suggestion": A suggestion for fixing the issue
            """
            
            # Use OpenAI to analyze code
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": code}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis = json.loads(response.choices[0].message.content)
            
            return analysis.get("issues", [])
        except Exception as e:
            print(f"Error analyzing code: {e}")
            return []
    
    def _repair_code(self, code, issues, language):
        """
        Repair code based on identified issues
        """
        try:
            # Create a system prompt for code repair
            system_prompt = f"""
            You are Riley, an advanced AI specialized in code repair.
            Fix the provided {language} code based on the identified issues.
            Return the complete fixed code, not just the changes.
            Maintain the original functionality while addressing the issues.
            Add comments explaining significant changes.
            """
            
            # Convert issues to string
            issues_str = json.dumps(issues)
            
            # Use OpenAI to repair code
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Code:\n\n{code}\n\nIssues:\n{issues_str}"}
                ]
            )
            
            # Extract the repaired code
            repaired_code = response.choices[0].message.content
            
            # If the response contains markdown code blocks, extract the code
            code_block_pattern = r"```(?:\w+)?\n([\s\S]*?)\n```"
            code_blocks = re.findall(code_block_pattern, repaired_code)
            
            if code_blocks:
                # Use the first code block
                repaired_code = code_blocks[0]
            
            return repaired_code
        except Exception as e:
            print(f"Error repairing code: {e}")
            return code
