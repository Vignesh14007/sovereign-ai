import subprocess
import sys
import tempfile
from pathlib import Path


TIMEOUT_SECONDS = 5


def run_python(code: str) -> dict:
    """
    Execute Python code in a temporary subprocess.

    This is a prototype sandbox layer:
    - Uses a separate subprocess
    - Enforces a short timeout
    - Captures stdout/stderr
    - Does not intentionally provide shell execution
    """

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(code)
            temp_file = Path(f.name)

        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=temp_file.parent,
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "stdout": "",
            "stderr": "Execution timed out.",
            "return_code": None,
        }

    except Exception as e:
        return {
            "status": "error",
            "stdout": "",
            "stderr": str(e),
            "return_code": None,
        }

    finally:
        if temp_file and temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    result = run_python("print(2 + 3)")
    print(result)
