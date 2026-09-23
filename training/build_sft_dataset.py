import json
import re
from pathlib import Path

SRC = Path("data/corpus/chunks/mrpl_sections_final.jsonl")
OUT = Path("data/training/mrpl_sft.jsonl")

def clean_text(text):
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\bMangalore Refinery And Petrochemicals Limited\b', 'MRPL', text, flags=re.I)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def sentences(text):
    text = clean_text(text)
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if len(p.strip()) > 35]

def summarize(text, section):
    s = sentences(text)

    # Prefer informative sentences over headings/legal boilerplate.
    bad = (
        "section 134", "companies act", "notification dated",
        "may be accessed", "website at", "annexure"
    )

    useful = [
        x for x in s
        if not any(b in x.lower() for b in bad)
    ]

    selected = useful[:3] if useful else s[:3]

    if not selected:
        return "The excerpt does not contain enough substantive information to provide a reliable summary."

    return " ".join(selected)

def extract(text, section):
    s = sentences(text)

    keywords = {
        "OPERATIONS": [
            "throughput", "production", "crude", "refinery", "yield",
            "capacity", "distillate", "energy", "power"
        ],
        "HSE": [
            "safety", "health", "incident", "emergency", "fire",
            "training", "occupational", "accident"
        ],
        "RISK": [
            "risk", "mitigation", "enterprise", "governance",
            "committee", "cyber", "security"
        ],
        "PROJECTS": [
            "project", "commissioned", "construction", "terminal",
            "capacity", "investment"
        ],
        "DIGITAL_IT": [
            "SAP", "digital", "software", "IT", "cyber",
            "technology", "automation"
        ],
        "ENVIRONMENT": [
            "environment", "emission", "water", "waste",
            "energy", "carbon", "renewable"
        ],
        "ENERGY_TECHNOLOGY": [
            "energy", "technology", "fuel", "efficiency",
            "consumption", "process"
        ],
        "MARKETING": [
            "sales", "marketing", "product", "retail",
            "customer", "outlet", "volume"
        ],
        "CSR": [
            "CSR", "community", "education", "health",
            "village", "women", "development"
        ],
    }

    keys = keywords.get(section, [
        "MRPL", "company", "policy", "management", "performance"
    ])

    matches = []
    for x in s:
        low = x.lower()
        if any(k.lower() in low for k in keys):
            if x not in matches:
                matches.append(x)

    matches = matches[:5]

    if not matches:
        matches = s[:3]

    return "\n".join(f"- {x}" for x in matches)

rows = []

with SRC.open("r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]

for r in chunks:
    text = r["text"]
    section = r["section"]

    rows.append({
        "instruction": f"Summarize the important {section.replace('_', ' ').lower()} information from this MRPL annual-report excerpt in 2-3 concise sentences.",
        "input": text,
        "output": summarize(text, section),
        "metadata": {
            "report": r["report"],
            "year": r["year"],
            "section": section,
            "chunk_id": r["chunk_id"],
            "task": "summary"
        }
    })

    rows.append({
        "instruction": f"Extract the most important factual points from this MRPL {section.replace('_', ' ').lower()} excerpt. Return at most 5 concise bullet points and do not add information that is not present in the excerpt.",
        "input": text,
        "output": extract(text, section),
        "metadata": {
            "report": r["report"],
            "year": r["year"],
            "section": section,
            "chunk_id": r["chunk_id"],
            "task": "extraction"
        }
    })

OUT.parent.mkdir(parents=True, exist_ok=True)

with OUT.open("w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("Source chunks:", len(chunks))
print("SFT examples:", len(rows))
print("Written:", OUT)
