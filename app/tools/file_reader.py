from pathlib import Path


# Only allow the agent to read files inside the project's data/input directory.
BASE_DIR = Path(__file__).resolve().parents[2]
ALLOWED_DIR = (BASE_DIR / "data" / "input").resolve()


def read_local_file(filename: str) -> str:
    """
    Safely read a text file from data/input.

    The path is restricted so the tool cannot read arbitrary
    files from the workstation.
    """
    requested_path = (ALLOWED_DIR / filename).resolve()

    # Prevent path traversal outside data/input
    if ALLOWED_DIR not in requested_path.parents:
        return "ERROR: Access denied. File is outside the allowed directory."

    if not requested_path.exists():
        return f"ERROR: File not found: {filename}"

    if not requested_path.is_file():
        return f"ERROR: Not a file: {filename}"

    try:
        return requested_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return "ERROR: File is not a UTF-8 text file."
    except Exception as e:
        return f"ERROR: Could not read file: {e}"


if __name__ == "__main__":
    print("FILE READER TOOL: READY")
