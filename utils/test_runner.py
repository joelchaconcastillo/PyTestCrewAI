import tempfile
import subprocess
import os
import uuid

def run_pytest(test_code_path: str):
    """
    Runs pytest on the provided test file and captures output.
    Returns a dictionary with:
        - passed: bool
        - stdout: str
        - stderr: str
    """
    if not os.path.exists(test_code_path):
        return {"passed": False, "stdout": "", "stderr": f"Test file {test_code_path} not found."}

    try:
        # Run pytest quietly (-q)
        result = subprocess.run(
            ["pytest", test_code_path, "-q", "--disable-warnings"],
            capture_output=True,
            text=True,
            timeout=20
        )
        return {
            "passed": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "stdout": "",
            "stderr": "Timeout expired while running pytest."
        }
    except Exception as e:
        return {
            "passed": False,
            "stdout": "",
            "stderr": f"Error running pytest: {e}"
        }
