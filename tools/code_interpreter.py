"""
Code Interpreter tool for executing Python code safely
"""
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any
import traceback


def run_python_code(code: str) -> str:
    """
    Execute Python code in a restricted environment and return the output.
    
    WARNING: This is a simplified implementation for demonstration.
    In production, use a proper sandboxed environment like:
    - Docker containers
    - PyPy sandbox
    - RestrictedPython
    - AWS Lambda or similar serverless functions
    """
    
    # Create restricted globals (limited built-ins)
    safe_builtins = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'len': len,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'map': map,
        'filter': filter,
        'sorted': sorted,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'print': print,
    }
    
    # Safe modules that can be imported
    safe_modules = {
        'math': __import__('math'),
        'datetime': __import__('datetime'),
        'json': __import__('json'),
    }
    
    restricted_globals = {
        '__builtins__': safe_builtins,
        **safe_modules
    }
    
    # Capture output
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    try:
        # Check for dangerous operations
        dangerous_keywords = ['import os', 'import sys', '__import__', 'eval', 'exec', 
                             'open', 'file', 'input', 'compile', '__']
        if any(keyword in code for keyword in dangerous_keywords):
            return "Error: Code contains restricted operations. Only basic math and data operations are allowed."
        
        # Redirect stdout and stderr
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            # Execute code
            exec(code, restricted_globals)
        
        # Get output
        output = stdout_capture.getvalue()
        errors = stderr_capture.getvalue()
        
        if errors:
            return f"Execution completed with warnings:\n{errors}\n\nOutput:\n{output}"
        elif output:
            return f"Execution successful:\n{output}"
        else:
            return "Code executed successfully (no output produced)."
    
    except Exception as e:
        error_trace = traceback.format_exc()
        return f"Error executing code:\n{str(e)}\n\nDetails:\n{error_trace}"


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    This is a simpler, more focused version for calculations.
    """
    try:
        # Only allow mathematical operations
        allowed_chars = set('0123456789+-*/().%** ')
        if not all(c in allowed_chars for c in expression.replace(' ', '')):
            return "Error: Expression contains invalid characters. Only numbers and operators (+, -, *, /, **, %, parentheses) are allowed."
        
        # Evaluate safely
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    
    except Exception as e:
        return f"Error in calculation: {str(e)}"


def calculate_compound_interest(principal: float, rate: float, time: float, compounds_per_year: int = 12) -> str:
    """
    Calculate compound interest.
    Formula: A = P(1 + r/n)^(nt)
    """
    try:
        principal = float(principal)
        rate = float(rate) / 100  # Convert percentage to decimal
        time = float(time)
        compounds_per_year = int(compounds_per_year)
        
        # Calculate compound interest
        amount = principal * ((1 + rate / compounds_per_year) ** (compounds_per_year * time))
        interest_earned = amount - principal
        
        result = f"""
Compound Interest Calculation:
- Principal Amount: ${principal:,.2f}
- Annual Interest Rate: {rate * 100}%
- Time Period: {time} years
- Compounding Frequency: {compounds_per_year} times per year

Final Amount: ${amount:,.2f}
Interest Earned: ${interest_earned:,.2f}
Total Return: {(interest_earned / principal * 100):.2f}%
"""
        return result.strip()
    
    except Exception as e:
        return f"Error calculating compound interest: {str(e)}"


def analyze_investment_returns(initial: float, final: float, years: float) -> str:
    """
    Analyze investment returns and calculate metrics.
    """
    try:
        initial = float(initial)
        final = float(final)
        years = float(years)
        
        if initial <= 0 or years <= 0:
            return "Error: Initial investment and years must be positive numbers."
        
        # Calculate metrics
        total_return = final - initial
        total_return_pct = (total_return / initial) * 100
        cagr = (((final / initial) ** (1 / years)) - 1) * 100
        
        result = f"""
Investment Return Analysis:
- Initial Investment: ${initial:,.2f}
- Final Value: ${final:,.2f}
- Time Period: {years} years

Total Return: ${total_return:,.2f} ({total_return_pct:.2f}%)
Compound Annual Growth Rate (CAGR): {cagr:.2f}%
Average Annual Return: {total_return_pct / years:.2f}% per year
"""
        return result.strip()
    
    except Exception as e:
        return f"Error analyzing returns: {str(e)}"

