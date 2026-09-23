import json
import urllib.request
from rag.retriever import retrieve

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:latest"

def ask_mistral(question, context):
    prompt = f"""You are an industrial document assistant.

Answer the user's question using ONLY the provided document evidence.

If the evidence does not contain the answer, say:
"I could not find this information in the provided documents."

Do not invent facts.
Do not make approval or safety decisions.
Clearly distinguish facts from recommendations.

DOCUMENT EVIDENCE:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"].strip()

def answer_question(question):
    results = retrieve(question, top_k=3, min_score=0.10)

    if not results:
        return "I could not find this information in the provided documents."

    context = "\n\n".join(
        f"[Source: {r['source']} | Relevance: {r['score']:.4f}]\n{r['text']}"
        for r in results
    )

    return ask_mistral(question, context)

if __name__ == "__main__":
    question = "What was the wall thickness measured at P3?"
    print(answer_question(question))
