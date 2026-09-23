import re


def _contains_term(text, term):
    if " " in term or "&" in term:
        return term in text

    return re.search(rf"\b{re.escape(term)}\b", text) is not None


def classify_task(request):
    text = request.lower()

    if any(_contains_term(text, word) for word in [
        "image", "photo", "photograph", "drawing", "diagram", "flow diagram", "process flow diagram", "engineering drawing", "engineering diagram", "pfd",
        "p&id", "pid", "scanned", "visual"
    ]):
        return "vision"

    if any(_contains_term(text, word) for word in [
        "python", "code", "script", "program",
        "csv", "dataframe", "sql", "calculate"
    ]):
        return "code"

    if any(_contains_term(text, word) for word in [
        "inspection", "maintenance", "report", "sop",
        "procedure", "manual", "document"
    ]):
        return "text"

    if any(_contains_term(text, word) for word in [
        "chat", "conversation", "discuss"
    ]):
        return "chat"

    return "text"


if __name__ == "__main__":
    tests = [
        "What is photosynthesis?",
        "Analyze this photo of equipment",
        "Analyze this P&ID",
        "Write Python code to calculate the average temperature",
        "Explain the inspection findings",
        "Let's discuss the maintenance report",
    ]

    for test in tests:
        print(f"{test} -> {classify_task(test)}")
