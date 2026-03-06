# executor.py

import subprocess
import tempfile
import os
import time
from languages import get_language_config

# The resource module allows us to track memory natively on Linux!
try:
    import resource
except ImportError:
    resource = None

def get_language_version(command):
    """Runs a terminal command to fetch the installed version of the language."""
    try:
        # e.g., runs `python3 --version`
        res = subprocess.run([command, "--version"], capture_output=True, text=True, timeout=2)
        # Some languages print version to stdout, others to stderr
        output = res.stdout.strip() or res.stderr.strip()
        # Grab just the first line to keep our badge clean
        return output.split('\n')[0] if output else "Version Unknown"
    except Exception:
        return "Version Unknown"

def execute_code(code, language="Python", user_input="", timeout_limit=5):
    config = get_language_config(language)
    if not config:
        return "Error: Language not supported.", 0.0, True, "Unknown", "N/A"

    extension = config["extension"]
    command = config["command"]

    # 1. Fetch the exact language version string
    version_str = get_language_version(command)

    with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    start_time = time.perf_counter() 
    is_error = False 
    
    try:
        result = subprocess.run(
            [command, temp_file_path],
            input=user_input,       
            capture_output=True,
            text=True,
            timeout=timeout_limit   
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n--- Errors ---\n{result.stderr}"
            is_error = True
            
        final_output = output if output else "Code executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        final_output = f"Error: Execution timed out (exceeded {timeout_limit} seconds). Infinite loop maybe?"
        is_error = True
    except Exception as e:
        final_output = f"An unexpected error occurred: {str(e)}"
        is_error = True
    finally:
        exec_time = time.perf_counter() - start_time 
        
        # 2. Fetch Peak Memory usage of child processes (Linux only)
        if resource:
            # ru_maxrss returns memory in Kilobytes on Linux
            peak_memory_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            memory_usage = f"{peak_memory_kb / 1024:.2f} MB"
        else:
            memory_usage = "N/A (Linux Required)"

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    # We now return FIVE things!
    return final_output, exec_time, is_error, version_str, memory_usage