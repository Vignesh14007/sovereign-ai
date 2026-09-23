import re


INDUSTRIAL_TERMS = [
    "mrpl",
    "mangalore refinery",
    "refinery",
    "crude oil",
    "crude",
    "petroleum",
    "petrochemical",
    "pfcc",
    "dcu",
    "refining",
    "refinery process",
    "throughput",
    "capacity utilization",
    "inspection",
    "maintenance",
    "sop",
    "p&id",
    "pid",
    "hse",
    "industrial",
    "plant",
    "equipment",
    "process unit",
    "process safety",
    "annual report",
    "shutdown",
    "turnaround",
    "compressor",
    "distillation",
    "reactor",
    "pipeline",
    "storage tank",
]


def is_industrial_query(request):
    text = request.lower()

    for term in INDUSTRIAL_TERMS:
        if " " in term or "&" in term:
            if term in text:
                return True
        elif re.search(rf"\b{re.escape(term)}\b", text):
            return True

    return False
