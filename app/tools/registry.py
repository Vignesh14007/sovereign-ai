from app.tools.file_reader import read_local_file
from app.tools.sandbox.executor import run_python
from app.tools.document_generator import create_inspection_note


TOOLS = {
    "read_local_file": {
        "description": "Read a text file from the approved local input directory.",
        "function": read_local_file,
    },
    "run_python": {
        "description": "Execute Python code in the local sandbox with a timeout.",
        "function": run_python,
    },
    "create_inspection_note": {
        "description": "Generate a local Word inspection review note.",
        "function": create_inspection_note,
    },
}


def get_tool(name: str):
    """Return a registered tool by name."""
    return TOOLS.get(name)


def list_tools():
    """Return the names of all registered tools."""
    return list(TOOLS.keys())


if __name__ == "__main__":
    print("AVAILABLE TOOLS:")
    for tool_name in list_tools():
        print("-", tool_name)
