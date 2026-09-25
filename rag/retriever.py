import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent

MRPL_CHUNKS = (
    BASE_DIR
    / "data"
    / "corpus"
    / "chunks"
    / "mrpl_sections_final.jsonl"
)

ADMIN_CHUNKS = (
    BASE_DIR
    / "data"
    / "knowledge"
    / "chunks"
    / "knowledge_chunks.jsonl"
)

LEGACY_DOCS = BASE_DIR / "rag" / "documents"


def load_chunks():
    chunks = []

    # ---------------------------------------------------------
    # 1. Existing MRPL annual-report chunks
    # ---------------------------------------------------------
    if MRPL_CHUNKS.exists():

        with MRPL_CHUNKS.open("r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                item = json.loads(line)

                chunks.append({
                    "source": (
                        f"{item['report']} | "
                        f"{item['section']} | "
                        f"{item['heading']}"
                    ),
                    "text": item["text"],
                    "year": item.get("year"),
                    "report": item.get("report"),
                    "section": item.get("section"),
                    "heading": item.get("heading"),
                    "document_id": None,
                    "source_type": "mrpl",
                })

    # ---------------------------------------------------------
    # 2. Admin-uploaded company knowledge
    # ---------------------------------------------------------
    if ADMIN_CHUNKS.exists():

        with ADMIN_CHUNKS.open("r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if not line:
                    continue

                item = json.loads(line)

                document_id = item.get("document_id", "unknown")

                chunks.append({
                    "source": (
                        f"Admin Knowledge | "
                        f"{document_id} | "
                        f"Chunk {item.get('chunk_index', 0)}"
                    ),
                    "text": item["text"],
                    "year": None,
                    "report": None,
                    "section": None,
                    "heading": None,
                    "document_id": document_id,
                    "source_type": "admin",
                })

    # ---------------------------------------------------------
    # 3. Existing inspection/demo documents
    # ---------------------------------------------------------
    if LEGACY_DOCS.exists():

        for path in sorted(LEGACY_DOCS.glob("*.txt")):

            text = path.read_text(
                encoding="utf-8"
            ).strip()

            if text:

                chunks.append({
                    "source": path.name,
                    "text": text,
                    "year": None,
                    "report": None,
                    "section": None,
                    "heading": None,
                    "document_id": None,
                    "source_type": "legacy",
                })

    return chunks


def retrieve(
    query,
    top_k=3,
    min_score=0.10
):
    """
    Search across the complete local knowledge base.

    Sources:
        - Prepared MRPL annual reports
        - Admin-uploaded company documents
        - Existing inspection/demo documents
    """

    chunks = load_chunks()

    if not chunks:
        return []

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(texts)

    query_vector = vectorizer.transform(
        [query]
    )

    scores = cosine_similarity(
        query_vector,
        matrix
    ).flatten()

    ranked = scores.argsort()[::-1]

    results = []

    for i in ranked:

        score = float(scores[i])

        if score < min_score:
            continue

        result = dict(chunks[i])

        result["score"] = score

        results.append(result)

        if len(results) >= top_k:
            break

    return results


if __name__ == "__main__":

    query = (
        "What was the crude throughput "
        "achieved during FY 2022-23?"
    )

    print(f"QUERY: {query}")

    for result in retrieve(query):

        print(
            f"\nSOURCE: {result['source']}"
        )

        print(
            f"SCORE: {result['score']:.4f}"
        )

        print(
            f"TYPE: {result['source_type']}"
        )

        print(
            result["text"][:1000]
        )
