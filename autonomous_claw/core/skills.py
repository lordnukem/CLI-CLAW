import subprocess
from typing import Dict, Any, Tuple

def execute_code_skill(command: str, cwd: str = ".") -> Tuple[int, str]:
    """
    Executes a shell command or script as the "Code Skill" for the agents.
    Returns the exit code and the stdout/stderr output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]\n{result.stderr}"
        return result.returncode, output.strip()
    except Exception as e:
        return 1, str(e)
