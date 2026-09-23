from app.agent.classifier import classify_task
from app.agent.domain import is_industrial_query
from app.models.router import select_model
from app.models.ollama_client import generate, generate_with_image
from app.tools.file_reader import read_local_file
from app.tools.sandbox.executor import run_python
from app.tools.document_generator import create_inspection_note
from rag.retriever import retrieve
from app.security.audit import log_event


def _extract_section(text: str, heading: str, next_heading: str | None = None):
    start = text.lower().find(heading.lower())
    if start == -1:
        return []

    section = text[start + len(heading):]

    if next_heading:
        end = section.lower().find(next_heading.lower())
        if end != -1:
            section = section[:end]

    items = []
    for line in section.splitlines():
        line = line.strip()
        if line.startswith(("-", "*")):
            value = line.lstrip("-* ").strip()
            if value:
                items.append(value)

    return items


def _extract_value(text: str, label: str):
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            if key.strip().lower() == label.lower():
                return value.strip()
    return ""


def _generate_inspection_note(request: str):
    results = retrieve(request, top_k=5, min_score=0.05)

    if not results:
        return {
            "task_type": "inspection_workflow",
            "model": None,
            "answer": "I could not find relevant inspection information in the provided documents."
        }

    context = "\n\n".join(item["text"] for item in results)

    prompt = f"""
You are a local industrial document-review assistant.

Create a structured inspection review from ONLY the document evidence below.

Extract:
1. Equipment
2. Inspection Date
3. Key Findings
4. Recommendations

Do not invent information.
If a field is unavailable, write "Not specified".

DOCUMENT EVIDENCE:
{context}

USER REQUEST:
{request}

Return exactly in this format:

Equipment: <value>
Inspection Date: <value>

FINDINGS:
- <finding>
- <finding>

RECOMMENDATIONS:
- <recommendation>
- <recommendation>
"""

    model = select_model("text")
    generated = generate(model, prompt).strip()

    equipment = _extract_value(generated, "Equipment")
    inspection_date = _extract_value(generated, "Inspection Date")

    findings = _extract_section(
        generated,
        "FINDINGS:",
        "RECOMMENDATIONS:"
    )

    recommendations = _extract_section(
        generated,
        "RECOMMENDATIONS:"
    )

    if not equipment:
        equipment = _extract_value(context, "Equipment")

    if not inspection_date:
        inspection_date = _extract_value(context, "Inspection Date")

    if not findings:
        findings = _extract_section(
            context,
            "Findings:",
            "Recommendations:"
        )

    if not recommendations:
        recommendations = _extract_section(
            context,
            "Recommendations:"
        )

    output_path = create_inspection_note(
        equipment=equipment or "Not specified",
        inspection_date=inspection_date or "Not specified",
        findings=findings or ["No structured findings were extracted."],
        recommendations=recommendations or ["No recommendations were extracted."]
    )

    return {
        "task_type": "inspection_workflow",
        "model": model,
        "generated_review": generated,
        "output": output_path,
        "answer": "Inspection review note generated successfully."
    }


def run_agent(request: str, image_path: str | None = None):
    task_type = classify_task(request)
    request_lower = request.lower()

    # Reject unrelated questions before any industrial tool/model processing.
    if task_type not in ("vision", "code") and not is_industrial_query(request):
        trace = [f"TASK CLASSIFIED: {task_type}"]
        trace.append("DOMAIN CHECK: non-industrial request")
        trace.append("RESULT: request rejected")

        return {
            "task_type": task_type,
            "model": None,
            "answer": "Please ask an industrial-related question.",
            "trace": trace
        }

    log_event({
        "event": "agent_request",
        "task_type": task_type,
        "request": request,
        "status": "started"
    })

    trace = [
        f"TASK CLASSIFIED: {task_type}"
    ]

    # ---------------------------------------------------------
    # TOOL 1: LOCAL FILE READER
    # ---------------------------------------------------------
    if request_lower.startswith("read file:"):
        filename = request.split(":", 1)[1].strip()
        content = read_local_file(filename)

        trace.append("TOOL: read_local_file")
        return {
            "task_type": "file_read",
            "model": None,
            "answer": content,
            "trace": trace
        }

    # ---------------------------------------------------------
    # TOOL 2: INSPECTION DOCUMENT WORKFLOW
    # ---------------------------------------------------------
    if (
        "inspection" in request_lower
        and any(phrase in request_lower for phrase in [
            "create inspection note",
            "create an inspection note",
            "create inspection review",
            "create an inspection review",
            "generate inspection note",
            "generate an inspection note",
            "generate inspection review",
            "generate an inspection review",
            "write inspection note",
            "write an inspection note",
            "approval note",
        ])
    ):
        result = _generate_inspection_note(request)
        result["trace"] = [
            f"TASK CLASSIFIED: {task_type}",
            "KNOWLEDGE: local RAG",
            f"MODEL SELECTED: {result['model']}",
            "TOOL: create_inspection_note",
            f"ARTIFACT: {result['output']}"
        ]

        log_event({
            "event": "agent_completed",
            "task_type": "inspection_workflow",
            "model": result["model"],
            "knowledge": "local_rag",
            "tool": "create_inspection_note",
            "artifact": result["output"],
            "status": "success",
        })

        return result

    # ---------------------------------------------------------
    # TOOL 3: LOCAL VISION
    # ---------------------------------------------------------
    if task_type == "vision":
        image_path = image_path or "data/input/inspection_test.png"
        model = select_model("vision")

        prompt = """You are a local multimodal industrial AI assistant.

Analyze the provided industrial image carefully.

Return a concise structured analysis with these headings:

IMAGE TYPE:
Identify what kind of industrial image/document this appears to be.

VISIBLE ELEMENTS:
List important equipment, components, labels, tables, diagrams, symbols,
or other clearly visible elements.

OBSERVATIONS:
Describe only what can actually be observed in the image.

POTENTIAL INDUSTRIAL RELEVANCE:
Explain at a high level what the visible information may relate to.

LIMITATIONS:
If a value, label, measurement, equipment ID, date, or other detail is
unclear or unreadable, explicitly say "Not clearly visible".

IMPORTANT:
- Do not invent facts.
- Do not guess exact measurements or hidden information.
- Do not make safety, maintenance, or approval decisions.
- Use only information visibly present in the image.
"""

        answer = generate_with_image(model, prompt, image_path)

        trace.extend([
            f"MODEL SELECTED: {model}",
            "TOOL: local vision analysis",
            "GROUNDING: exact facts must come from local documents/RAG"
        ])

        log_event({
            "event": "agent_completed",
            "task_type": "vision",
            "model": model,
            "tool": "local_vision_analysis",
            "status": "success"
        })

        return {
            "task_type": "vision",
            "model": model,
            "answer": answer,
            "trace": trace
        }

    # ---------------------------------------------------------
    # TOOL 3: PYTHON SANDBOX
    # ---------------------------------------------------------
    if task_type == "code":

        prompt = f"""
You are a local coding assistant.

The user has requested:

{request}

Return ONLY executable Python code.
Do not explain the code.
Do not use markdown.
Do not use shell commands.
Do not access the internet.
Do not read files unless explicitly provided by the user.
Always print the final result.
"""

        model = select_model("code")
        generated_code = generate(model, prompt).strip()

        if "```" in generated_code:
            parts = generated_code.split("```")
            if len(parts) >= 2:
                generated_code = parts[1].strip()
                if generated_code.startswith("python"):
                    generated_code = generated_code[6:].lstrip()
        else:
            lines = generated_code.splitlines()
            code_lines = []

            for line in lines:
                stripped = line.strip()
                if (
                    stripped.startswith(("result =", "print(", "import ", "from "))
                    or "=" in stripped
                ):
                    code_lines.append(line)

            generated_code = "\n".join(code_lines).strip()

        execution = run_python(generated_code)

        log_event({
            "event": "agent_completed",
            "task_type": "code",
            "model": model,
            "tool": "run_python",
            "execution_status": execution["status"],
            "status": "success" if execution["status"] == "success" else "failed"
        })

        trace.extend([
            f"MODEL SELECTED: {model}",
            "TOOL: run_python",
            f"EXECUTION: {execution['status']}"
        ])

        return {
            "task_type": "code",
            "model": model,
            "generated_code": generated_code,
            "execution": execution,
            "answer": execution["stdout"]
            if execution["status"] == "success"
            else execution["stderr"],
            "trace": trace
        }

    # ---------------------------------------------------------
    # TOOL 4: TEXT + RAG WORKFLOW
    # ---------------------------------------------------------
    if task_type == "text":
        results = retrieve(request, top_k=3, min_score=0.10)

        if not results:
            return {
                "task_type": task_type,
                "model": None,
                "answer": "I could not find this information in the provided documents.",
                "trace": trace + ["KNOWLEDGE: local RAG", "RESULT: no relevant evidence"]
            }

        context = "\n\n".join(
            item["text"] for item in results
        )

        prompt = f"""
You are a local sovereign industrial AI assistant.

Answer the user's question using ONLY the provided document evidence.

Rules:
- Do not invent information.
- If the evidence does not contain the answer, say so.
- Clearly distinguish documented facts from recommendations.
- Do not make safety or approval decisions.

DOCUMENT EVIDENCE:
{context}

USER QUESTION:
{request}

ANSWER:
"""

        model = select_model("text")
        answer = generate(model, prompt)

        trace.extend([
            "KNOWLEDGE: local RAG",
            f"MODEL SELECTED: {model}"
        ])

        log_event({
            "event": "agent_completed",
            "task_type": task_type,
            "model": model,
            "knowledge": "local_rag",
            "status": "success"
        })

        return {
            "task_type": task_type,
            "model": model,
            "answer": answer,
            "trace": trace
        }

    # ---------------------------------------------------------
    # OTHER TASK TYPES
    # ---------------------------------------------------------
    model = select_model(task_type)

    answer = generate(
        model,
        f"""
You are a local sovereign AI assistant.

User request:
{request}

Respond helpfully and do not claim to have performed actions
that you did not actually perform.
"""
    )

    trace.append(f"MODEL SELECTED: {model}")

    return {
        "task_type": task_type,
        "model": model,
        "answer": answer,
        "trace": trace
    }


if __name__ == "__main__":
    result = run_agent(
        "Create an inspection review note for the HX-101 inspection report."
    )

    print("TASK:", result["task_type"])
    print("MODEL:", result["model"])
    print("ANSWER:", result["answer"])

    if "output" in result:
        print("OUTPUT:", result["output"])
