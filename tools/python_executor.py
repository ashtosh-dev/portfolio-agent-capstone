import subprocess
import tempfile
import os

def execute_python_code(code: str) -> str:
    """Executes a Python code block and returns its standard output and error.

    Use this tool to run complex quantitative analyses, calculations, and data processing.
    The code runs in a separate process. You should write complete, self-contained Python scripts.
    Include print statements to inspect outputs and variables.

    Args:
        code (str): The complete Python source code block to execute.
    """
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(code)
        temp_file_name = f.name
    
    try:
        result = subprocess.run(
            ["python3", temp_file_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nExit Code: {result.returncode}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out (limit: 30 seconds)."
    except Exception as e:
        return f"Error executing code: {str(e)}"
    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
