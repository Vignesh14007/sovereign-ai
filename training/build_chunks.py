from pathlib import Path
import json
import re
from collections import Counter

INPUT_DIR = Path("data/corpus/clean")
OUTPUT = Path("data/corpus/chunks/mrpl_sections.jsonl")

TARGET_CHARS = 5000
MAX_CHARS = 7000
OVERLAP_CHARS = 700

SECTION_PATTERNS = [
    ("OPERATIONS", r"^OPERATIONAL PERFORMANCE FOR FY \d{4}-\d{2}$"),
    ("MARKETING", r"^MARKETING AND BUSINESS DEVELOPMENT$"),
    ("PROJECTS", r"^PROJECTS$"),
    ("DIGITAL_IT", r"^DEVELOPMENT OF INFORMATION TECHNOLOGY, SOFTWARE, HARDWARE ETC\.?$"),
    ("HSE", r"^HEALTH, SAFETY & ENVIRONMENT PERFORMANCE$"),
    ("SUSTAINABILITY", r"^SUSTAINABILITY INITIATIVES$"),
    ("CSR", r"^CORPORATE SOCIAL RESPONSIBILITY AND SUSTAINABILITY DEVELOPMENT$"),
    ("HUMAN_RESOURCES", r"^HUMAN RESOURCES$"),
    ("SECURITY", r"^SECURITY MEASURES$"),
    ("VIGILANCE", r"^VIGILANCE FUNCTION$"),
    ("WHISTLE_BLOWER", r"^WHISTLE BLOWER POLICY:?$"),
    ("ENERGY_TECHNOLOGY", r"^CONSERVATION OF ENERGY.*$"),
    ("RISK", r"^RISK MANAGEMENT POLICY\s*:??$"),
    ("INTERNAL_CONTROL", r"^INTERNAL FINANCIAL CONTROL\s*:??$"),
    ("MDA", r"^MANAGEMENT DISCUSSION AND ANALYSIS\s*:??$"),
    ("CORPORATE_GOVERNANCE", r"^CORPORATE GOVERNANCE\s*:??$"),
    ("BRSR", r"^BUSINESS RESPONSIBILITY AND SUSTAINABILITY REPORT\s*:??$"),
    ("ACKNOWLEDGEMENT", r"^ACKNOWLEDGEMENT$"),
]

COMPILED = [(name, re.compile(pattern, re.I)) for name, pattern in SECTION_PATTERNS]

def detect_section(line):
    text = line.strip()
    for name, pattern in COMPILED:
        if pattern.fullmatch(text):
            return name
    return None

def year_from_filename(path):
    m = re.search(r"_(\d{4})_(\d{2})_clean\.txt$", path.name)
    return m.group(1) if m else "unknown"

def chunk_text(text):
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = []
    current_len = 0

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if current and current_len + len(paragraph) > MAX_CHARS:
            chunks.append("\n\n".join(current))

            overlap = []
            overlap_len = 0
            for p in reversed(current):
                if overlap_len + len(p) > OVERLAP_CHARS:
                    break
                overlap.insert(0, p)
                overlap_len += len(p)

            current = overlap
            current_len = overlap_len

        current.append(paragraph)
        current_len += len(paragraph)

        if current_len >= TARGET_CHARS:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0

    if current:
        chunks.append("\n\n".join(current))

    return chunks

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

records = []

for path in sorted(INPUT_DIR.glob("*_clean.txt")):
    lines = path.read_text(encoding="utf-8").splitlines()
    year = year_from_filename(path)

    # Main Board Report only: Operational Performance -> before Annexure A
    start = next(
        (i for i, line in enumerate(lines)
         if re.fullmatch(r"OPERATIONAL PERFORMANCE FOR FY \d{4}-\d{2}", line.strip(), re.I)),
        None
    )

    end = next(
        (i for i, line in enumerate(lines)
         if re.fullmatch(r"ANNEXURE\s*-?\s*A", line.strip(), re.I) and start is not None and i > start),
        len(lines)
    )

    if start is None:
        print(f"WARNING: no Board Report start found in {path.name}")
        continue

    main_lines = lines[start:end]

    # Find section headings only inside this main Board Report range.
    boundaries = []

    for i, line in enumerate(main_lines):
        section = detect_section(line)
        if section:
            boundaries.append((i, section, line.strip()))

    # Keep only the first occurrence of each section.
    seen = set()
    sections = []

    for boundary in boundaries:
        if boundary[1] not in seen:
            seen.add(boundary[1])
            sections.append(boundary)

    # Create chunks for each section.
    for idx, (section_start, section, heading) in enumerate(sections):
        section_end = (
            sections[idx + 1][0]
            if idx + 1 < len(sections)
            else len(main_lines)
        )

        section_text = "\n".join(
            main_lines[section_start:section_end]
        ).strip()

        for chunk_id, chunk in enumerate(chunk_text(section_text)):
            records.append({
                "report": path.stem.replace("_clean", ""),
                "year": year,
                "section": section,
                "heading": heading,
                "chunk_id": chunk_id,
                "text": chunk,
                "tokens": len(chunk.split()),
            })

with OUTPUT.open("w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

counts = Counter(r["section"] for r in records)

print(f"Created: {OUTPUT}")
print(f"Total chunks: {len(records)}")
print("\nChunks by section:")
for section, count in counts.most_common():
    print(f"{section:25} {count}")

print("\nChunks by report:")
for report in sorted(set(r["report"] for r in records)):
    count = sum(r["report"] == report for r in records)
    print(f"{report:40} {count}")

print("\nTotal tokens:", sum(r["tokens"] for r in records))
