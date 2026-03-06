# executor.py

import subprocess
import tempfile
import os
import time
from languages import get_language_config

try:
    import resource
except ImportError:
    resource = None

def get_language_version(version_cmd):
    if not version_cmd:
        return "Version Unknown"
    try:
        res = subprocess.run(version_cmd, capture_output=True, text=True, timeout=2)
        output = res.stdout.strip() or res.stderr.strip()
        return output.split('\n')[0] if output else "Version Unknown"
    except Exception:
        return "Version Unknown"

def execute_code(code, language="Python", user_input="", timeout_limit=5):
    config = get_language_config(language)
    if not config:
        return "Error: Language not supported.", 0.0, True, "Unknown", "N/A"

    # Use a Temporary Directory to hold files and compiled binaries safely
    with tempfile.TemporaryDirectory() as temp_dir:
        # Java requires the file to match the class name exactly
        file_name = "Main.java" if language == "Java" else f"main{config['extension']}"
        file_path = os.path.join(temp_dir, file_name)
        
        with open(file_path, 'w') as f:
            f.write(code)

        version_str = get_language_version(config.get("version_cmd"))
        
        # --- COMPILATION STEP (C, C++, Java) ---
        if config.get("compile_cmd"):
            compile_cmd = [arg.format(file=file_path, dir=temp_dir) for arg in config["compile_cmd"]]
            try:
                comp_res = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
                if comp_res.returncode != 0:
                    return f"--- Compilation Error ---\n{comp_res.stderr}", 0.0, True, version_str, "N/A"
            except Exception as e:
                return f"Compilation Failed: {str(e)}", 0.0, True, version_str, "N/A"

        # --- EXECUTION STEP ---
        run_cmd = [arg.format(file=file_path, dir=temp_dir) for arg in config["run_cmd"]]
        start_time = time.perf_counter()
        is_error = False
        
        try:
            result = subprocess.run(run_cmd, input=user_input, capture_output=True, text=True, timeout=timeout_limit)
            output = result.stdout
            if result.stderr:
                output += f"\n--- Errors ---\n{result.stderr}"
                is_error = result.returncode != 0
            final_output = output if output else "Code executed successfully with no output."
            
        except subprocess.TimeoutExpired:
            final_output = f"Error: Execution timed out (exceeded {timeout_limit} seconds)."
            is_error = True
        except Exception as e:
            final_output = f"An unexpected error occurred: {str(e)}"
            is_error = True
        finally:
            exec_time = time.perf_counter() - start_time
            if resource:
                peak_memory_kb = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                memory_usage = f"{peak_memory_kb / 1024:.2f} MB"
            else:
                memory_usage = "N/A"

    return final_output, exec_time, is_error, version_str, memory_usage