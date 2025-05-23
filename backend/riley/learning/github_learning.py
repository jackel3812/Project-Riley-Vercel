import os
import tempfile
import subprocess
import json
from openai import OpenAI

class GitHubLearning:
    def __init__(self):
        """
        Initialize the GitHub learning
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def analyze_repo(self, repo_url):
        """
        Clone a GitHub repository and analyze its code structure and patterns
        """
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Clone the repository
                clone_result = self._clone_repo(repo_url, temp_dir)
                
                if 'error' in clone_result:
                    return clone_result
                
                # Analyze the repository structure
                structure = self._analyze_repo_structure(temp_dir)
                
                # Analyze code patterns
                patterns = self._analyze_code_patterns(temp_dir)
                
                # Generate insights
                insights = self._generate_insights(structure, patterns, repo_url)
                
                return {
                    "repo_url": repo_url,
                    "structure": structure,
                    "patterns": patterns,
                    "insights": insights
                }
        except Exception as e:
            print(f"Error in GitHub learning: {e}")
            return {
                "error": "Failed to analyze repository",
                "details": str(e)
            }
    
    def _clone_repo(self, repo_url, target_dir):
        """
        Clone a GitHub repository to the target directory
        """
        try:
            # Run git clone command
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, target_dir],
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                "status": "success",
                "message": "Repository cloned successfully"
            }
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
            return {
                "error": "Failed to clone repository",
                "details": e.stderr
            }
    
    def _analyze_repo_structure(self, repo_dir):
        """
        Analyze the structure of the repository
        """
        try:
            # Get list of files
            result = subprocess.run(
                ["find", repo_dir, "-type", "f", "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.ts", "-o", "-name", "*.jsx", "-o", "-name", "*.tsx"],
                capture_output=True,
                text=True,
                check=True
            )
            
            files = result.stdout.strip().split('\n')
            
            # Count files by type
            file_types = {}
            for file in files:
                if file:
                    ext = os.path.splitext(file)[1]
                    file_types[ext] = file_types.get(ext, 0) + 1
            
            # Get directory structure
            dir_structure = {}
            for file in files:
                if file:
                    rel_path = os.path.relpath(file, repo_dir)
                    parts = rel_path.split(os.path.sep)
                    
                    current = dir_structure
                    for i, part in enumerate(parts[:-1]):
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    
                    current[parts[-1]] = None
            
            return {
                "file_count": len(files),
                "file_types": file_types,
                "directory_structure": dir_structure
            }
        except Exception as e:
            print(f"Error analyzing repository structure: {e}")
            return {
                "error": "Failed to analyze repository structure",
                "details": str(e)
            }
    
    def _analyze_code_patterns(self, repo_dir):
        """
        Analyze code patterns in the repository
        """
        try:
            # Sample a few files for analysis
            result = subprocess.run(
                ["find", repo_dir, "-type", "f", "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.ts"],
                capture_output=True,
                text=True,
                check=True
            )
            
            files = result.stdout.strip().split('\n')
            
            # Sample up to 5 files
            sample_files = files[:5] if len(files) > 5 else files
            
            # Read file contents
            file_contents = {}
            for file in sample_files:
                if file:
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            file_contents[os.path.relpath(file, repo_dir)] = content
                    except Exception as e:
                        print(f"Error reading file {file}: {e}")
            
            # Analyze patterns using OpenAI
            patterns = self._analyze_patterns_with_openai(file_contents)
            
            return patterns
        except Exception as e:
            print(f"Error analyzing code patterns: {e}")
            return {
                "error": "Failed to analyze code patterns",
                "details": str(e)
            }
    
    def _analyze_patterns_with_openai(self, file_contents):
        """
        Use OpenAI to analyze code patterns in the files
        """
        try:
            # Prepare the content for analysis
            content_text = ""
            for file_path, content in file_contents.items():
                content_text += f"\n\n--- {file_path} ---\n{content[:2000]}"  # Limit content size
            
            # Create a system prompt for pattern analysis
            system_prompt = """
            You are Riley, an advanced AI specialized in code analysis.
            Analyze the provided code samples and identify:
            1. Design patterns used
            2. Code organization approaches
            3. Common libraries and frameworks
            4. Coding style and conventions
            5. Potential best practices to learn
            
            Format the response as a structured JSON object with these categories.
            """
            
            # Use OpenAI to analyze patterns
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze these code samples:\n{content_text}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            patterns = json.loads(response.choices[0].message.content)
            
            return patterns
        except Exception as e:
            print(f"Error in OpenAI pattern analysis: {e}")
            return {
                "error": "Failed to analyze patterns with OpenAI",
                "details": str(e)
            }
    
    def _generate_insights(self, structure, patterns, repo_url):
        """
        Generate insights based on the repository analysis
        """
        try:
            # Prepare the content for insight generation
            analysis_json = json.dumps({
                "structure": structure,
                "patterns": patterns,
                "repo_url": repo_url
            })
            
            # Create a system prompt for insight generation
            system_prompt = """
            You are Riley, an advanced AI specialized in code analysis and learning.
            Based on the repository analysis, generate insights on:
            1. Key architectural decisions
            2. Potential learning opportunities
            3. Best practices identified
            4. Suggestions for code improvements
            5. Overall assessment of code quality
            
            Format the response as a structured JSON object with these categories.
            """
            
            # Use OpenAI to generate insights
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate insights based on this repository analysis:\n{analysis_json}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            insights = json.loads(response.choices[0].message.content)
            
            return insights
        except Exception as e:
            print(f"Error generating insights: {e}")
            return {
                "error": "Failed to generate insights",
                "details": str(e)
            }
