import os
import json
from openai import OpenAI
import sympy as sp
import re

class EquationSolver:
    def __init__(self):
        """
        Initialize the equation solver
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('RILEY_MODEL', 'gpt-4o')
    
    def solve(self, equation, output_format='text'):
        """
        Solve an equation or mathematical problem
        
        Args:
            equation (str): The equation or problem to solve
            output_format (str): Output format (text, latex, steps)
            
        Returns:
            dict: Solution information
        """
        try:
            # Try to solve with SymPy first for simple equations
            sympy_solution = self._solve_with_sympy(equation)
            
            if sympy_solution and 'error' not in sympy_solution:
                # If SymPy solved it successfully, return the result
                if output_format == 'latex':
                    # Convert to LaTeX if requested
                    sympy_solution['latex'] = self._convert_to_latex(sympy_solution['solution'])
                
                return sympy_solution
            
            # If SymPy failed or for more complex problems, use OpenAI
            return self._solve_with_openai(equation, output_format)
        except Exception as e:
            print(f"Error solving equation: {e}")
            return {
                "error": "Failed to solve equation",
                "details": str(e)
            }
    
    def _solve_with_sympy(self, equation):
        """
        Attempt to solve the equation using SymPy
        """
        try:
            # Check if it's a simple equation with = sign
            if '=' in equation:
                # Parse the equation
                left_side, right_side = equation.split('=', 1)
                
                # Try to identify the variable
                variables = set(re.findall(r'[a-zA-Z]', equation))
                
                # Remove common mathematical constants
                variables.discard('e')  # Euler's number
                variables.discard('i')  # Imaginary unit
                variables.discard('j')  # Imaginary unit (engineering notation)
                variables.discard('π')  # Pi
                variables.discard('pi') # Pi (text)
                
                if len(variables) == 1:
                    # If there's exactly one variable, solve for it
                    var = list(variables)[0]
                    var_sym = sp.Symbol(var)
                    
                    # Convert the equation to SymPy expression
                    expr = sp.sympify(left_side) - sp.sympify(right_side)
                    
                    # Solve the equation
                    solutions = sp.solve(expr, var_sym)
                    
                    if solutions:
                        return {
                            "equation": equation,
                            "variable": var,
                            "solution": str(solutions),
                            "method": "symbolic"
                        }
            
            # For expressions without = sign, try to simplify
            expr = sp.sympify(equation)
            simplified = sp.simplify(expr)
            
            return {
                "expression": equation,
                "simplified": str(simplified),
                "method": "simplification"
            }
        except Exception as e:
            print(f"SymPy error: {e}")
            return {"error": f"SymPy error: {str(e)}"}
    
    def _solve_with_openai(self, equation, output_format):
        """
        Solve the equation using OpenAI
        """
        try:
            # Create a system prompt based on the requested format
            if output_format == 'steps':
                system_prompt = """
                You are Riley, an advanced AI specialized in solving mathematical problems.
                Solve the given equation or problem step by step.
                Explain each step clearly and provide the final answer.
                Format the response as a JSON object with:
                1. "equation": The original equation
                2. "steps": An array of step-by-step explanations
                3. "solution": The final answer
                4. "method": The method used to solve the problem
                """
            elif output_format == 'latex':
                system_prompt = """
                You are Riley, an advanced AI specialized in solving mathematical problems.
                Solve the given equation or problem and provide the solution in LaTeX format.
                Format the response as a JSON object with:
                1. "equation": The original equation
                2. "solution": The solution in plain text
                3. "latex": The solution in LaTeX format
                4. "method": The method used to solve the problem
                """
            else:
                system_prompt = """
                You are Riley, an advanced AI specialized in solving mathematical problems.
                Solve the given equation or problem concisely.
                Format the response as a JSON object with:
                1. "equation": The original equation
                2. "solution": The solution
                3. "method": The method used to solve the problem
                """
            
            # Use OpenAI to solve the equation
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Solve this: {equation}"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            solution = json.loads(response.choices[0].message.content)
            
            return solution
        except Exception as e:
            print(f"OpenAI error: {e}")
            return {
                "error": "Failed to solve with OpenAI",
                "details": str(e)
            }
    
    def _convert_to_latex(self, solution_text):
        """
        Convert a solution to LaTeX format
        """
        try:
            # Use OpenAI to convert to LaTeX
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Convert the mathematical expression to LaTeX format."},
                    {"role": "user", "content": solution_text}
                ]
            )
            
            latex = response.choices[0].message.content.strip()
            
            # Remove any markdown backticks if present
            latex = re.sub(r'^```latex\s*|\s*```$', '', latex)
            
            return latex
        except Exception as e:
            print(f"LaTeX conversion error: {e}")
            return solution_text  # Return original text if conversion fails
