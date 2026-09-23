import json
import re
from pathlib import Path

src = Path("data/corpus/chunks/mrpl_sections_filtered.jsonl")
dst = Path("data/corpus/chunks/mrpl_sections_clean.jsonl")

rows = [json.loads(x) for x in src.open(encoding="utf-8")]

headers = {
    "Mangalore Reﬁnery And Petrochemicals Limited",
    "MANGALORE REFINERY AND PETROCHEMICALS LIMITED",
}

ligatures = {
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬃ": "ffi",
    "ﬀ": "ff",
}

out = []
removed_pages = 0
removed_headers = 0
lig_count = 0

for r in rows:
    text = r["text"]

    for old, new in ligatures.items():
        lig_count += text.count(old)
        text = text.replace(old, new)

    cleaned_lines = []

    for line in text.splitlines():
        if re.fullmatch(r"\s*\d{1,3}\s*", line):
            removed_pages += 1
            continue

        if line.strip() in headers:
            removed_headers += 1
            continue

        cleaned_lines.append(line)

    text = re.sub(r"\n{3,}", "\n\n", "\n".join(cleaned_lines)).strip()

    r["text"] = text
    r["tokens"] = len(text.split())
    out.append(r)

dst.write_text(
    "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out),
    encoding="utf-8",
)

print("Chunks:", len(out))
print("Page-number lines removed:", removed_pages)
print("Repeated headers removed:", removed_headers)
print("Ligature characters normalized:", lig_count)
print("Written:", dst)
