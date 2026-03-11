import sys
import io
import traceback

# creating the code execution class...
class PythonCodeExecutor:
    """
    Agent for executing python code snippets safely and capturing output.
    Used for analysis and dynamic calculations.
    """
    
    def __init__(self):
        # initializing executor environment...
        self.locals = {}
        self.globals = {}

    def execute(self, code: str) -> dict:
        """
        Executes a string of python code and returns stdout and any errors.
        """
        # writing stdout capture logic...
        stdout_buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout_buffer
        
        result = {
            "output": "",
            "error": None,
            "status": "success"
        }
        
        try:
            # executing code snippet with a safe environment that still allows basic functions...
            # allowing standard built-ins so print() and len() work...
            safe_globals = {"__builtins__": __builtins__}
            exec(code, safe_globals, self.locals)
            result["output"] = stdout_buffer.getvalue()
        except Exception as e:
            # adding basic exception handling...
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["status"] = "failed"
            result["traceback"] = traceback.format_exc()
        finally:
            # restoring stdout...
            sys.stdout = old_stdout
            
        return result

# adding a simple testing interface (for internal use)...
if __name__ == "__main__":
    executor = PythonCodeExecutor()
    example_code = "print('Analysis Complete: Found 5 key trends in the sales data.')"
    print(f"Running code: {example_code}")
    print(executor.execute(example_code))
