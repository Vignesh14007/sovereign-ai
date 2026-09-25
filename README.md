# 🛡️ Sovereign AI Workbench

### An On-Premise Agentic Multimodal AI Platform for Confidential Industrial Intelligence

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-Local%20Knowledge%20Grounding-6A5ACD?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational%20Prototype-lightgrey?style=for-the-badge)

> **Sovereign AI Workbench** is a prototype industrial AI platform designed around local inference, local enterprise knowledge, controlled tool execution, multimodal inspection workflows, role-based access, and auditability.

---

## 🎯 Project Overview

**Sovereign AI Workbench** is developed for **Smart India Hackathon 2026 — SIH26117**, under the problem context provided by **Mangalore Refinery and Petrochemicals Limited (MRPL)**.

Industrial organizations work with information spread across:

- 📊 Sensor and time-series data
- 🗄️ SQL databases
- 📝 Maintenance records
- 📘 Standard Operating Procedures (SOPs)
- 📚 Technical manuals
- 📄 Inspection reports
- 🖼️ Engineering drawings and inspection images
- 🧾 Operational logs
- ⚠️ Failure history
- 📑 Internal documents and reports

The challenge is not simply storing this information. The challenge is connecting the relevant sources when an engineer investigates a real operational question.

For example:

> **“Why did Compressor C-204 show abnormal behavior last week?”**

A useful investigation may require structured data analysis, document retrieval, historical maintenance information, visual inspection evidence, and verification of the final response.

Sovereign AI Workbench is designed to provide this workflow through a **controlled local AI environment** rather than depending on an external AI inference API.

---

# 🧩 Problem Statement

### SIH26117

**Problem Statement:**  
**Sovereign On-Premise Agentic AI Workbench using Open-Weight Multimodal LLMs for Confidential Industrial Work**

**Organization:** Mangalore Refinery and Petrochemicals Limited (MRPL)  
**Category:** Software  
**Theme:** Smart Automation

### Core Problem

Industrial information is fragmented across multiple systems and formats. Conventional chat interfaces generally answer from a single context and do not provide a controlled workflow for:

1. Understanding an industrial request
2. Selecting the appropriate capability
3. Retrieving authorized knowledge
4. Querying structured information
5. Executing controlled tools
6. Processing visual evidence
7. Correlating evidence
8. Producing an auditable response

At the same time, confidential industrial information may require deployment within an organization's controlled infrastructure.

---

# 💡 Our Solution

Sovereign AI Workbench brings together:

**Local LLMs + Agent Orchestration + RAG + Multimodal AI + Tool Execution + RBAC + Audit History**

Instead of a simple:

```text
User → Chatbot → Answer
```

the target architecture is:

```text
User
  ↓
Authentication & Authorization
  ↓
AI Workbench
  ↓
Task Classification
  ↓
Agent / Capability Selection
  ├── Knowledge / RAG
  ├── Structured Data
  ├── Code / Calculation
  ├── Vision
  └── Inspection Review
  ↓
Local Tools & Authorized Data
  ↓
Evidence / Result Processing
  ↓
Local LLM Response Generation
  ↓
History / Audit Record
  ↓
User
```

The current prototype implements the foundation of this architecture and is designed to be extended into a broader multi-agent industrial workbench.

---

# 🤖 What Makes It Agentic?

The system is designed around **task-driven orchestration**, rather than treating every request as ordinary chat.

A request can be classified according to the required capability.

### Example

```text
User:
"Review this compressor inspection note and identify relevant
maintenance information."
```

The orchestrator can:

```text
1. Understand request
        ↓
2. Classify task
        ↓
3. Select local capability/model
        ↓
4. Retrieve relevant knowledge
        ↓
5. Process the request
        ↓
6. Generate result
        ↓
7. Create an output artifact when required
        ↓
8. Record the operation in employee history
```

The architecture is intentionally modular so additional agents and tools can be introduced without replacing the complete application.

---

# 🏗️ Current Architecture

```text
                         ┌─────────────────────────┐
                         │       Streamlit UI      │
                         │ Authentication / RBAC   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     AI Orchestrator     │
                         │ Task Classification     │
                         │ Capability Selection    │
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼────────────────────────┐
              │                       │                        │
              ▼                       ▼                        ▼
       ┌─────────────┐        ┌──────────────┐         ┌──────────────┐
       │ Local LLM   │        │ Local RAG    │         │ Vision Model │
       │   Ollama    │        │ Knowledge    │         │   LLaVA      │
       │   Mistral   │        │ Retrieval    │         │              │
       └──────┬──────┘        └──────┬───────┘         └──────────────┘
              │                      │
              └──────────────┬───────┘
                             ▼
                  ┌──────────────────────┐
                  │ Controlled Local     │
                  │ Tools / Documents    │
                  │ / Database           │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Response + Artifact  │
                  │ + Employee History   │
                  └──────────────────────┘
```

---

# 🔐 Sovereignty & Privacy Design

The central design principle is to keep AI processing and enterprise knowledge inside the organization's controlled infrastructure.

### Local inference

The prototype uses locally hosted models through **Ollama**.

```text
Application
    ↓
localhost:11434
    ↓
Ollama
    ↓
Local Model
    ↓
Local Response
```

The application does not require an external cloud AI API for its core inference workflow.

### Important deployment principle

The prototype is **designed for controlled on-premise deployment**.

A production MRPL deployment would additionally require organization-approved:

- Network isolation
- Firewall / egress controls
- Secrets management
- Container or OS sandboxing
- Identity integration
- Centralized audit infrastructure
- Security monitoring
- Backup and recovery
- Model governance

The prototype therefore avoids claiming that the current development environment is automatically a fully air-gapped production system.

---

# 🧠 Local LLM Layer

The prototype is designed around open-weight models hosted locally.

### Text Model

Current prototype model:

```text
Mistral 7B-class model
↓
Ollama
↓
Local inference
```

### Vision Model

Current multimodal capability:

```text
LLaVA
↓
Local image understanding
```

The architecture can later support additional local models and task-based model routing.

---

# 📚 Local RAG Knowledge System

The Workbench includes a local knowledge-management and retrieval layer.

### Knowledge pipeline

```text
PDF / DOCX / TXT
       ↓
Document Ingestion
       ↓
Text Extraction
       ↓
Cleaning
       ↓
Section-Aware Chunking
       ↓
Metadata
       ↓
Local Knowledge Store
       ↓
Retriever
       ↓
Relevant Evidence
       ↓
Local LLM
       ↓
Grounded Answer
```

### Current retrieval approach

The prototype uses:

- TF-IDF retrieval
- Unigram + bigram features
- Cosine similarity
- Top-k retrieval
- Minimum relevance threshold
- Section-aware document chunks

The retrieval layer is intentionally modular so vector embeddings and a local vector database can be introduced later.

---

# 🏭 MRPL Knowledge Demonstration

The prototype has been tested with publicly available MRPL annual-report material.

The knowledge pipeline has processed four annual reports covering:

- FY 2022–23
- FY 2023–24
- FY 2024–25
- FY 2025–26

The current prototype extracts relevant sections and creates a compact retrieval corpus.

### Example grounded question

```text
What was the highest gross crude throughput achieved by MRPL
in FY 2022-23, and what were the PFCC and DCU capacity utilizations?
```

The validated prototype response uses retrieved document evidence rather than requiring the model to rely only on its internal knowledge.

### Grounding principle

If the requested information is not available in the supplied knowledge base, the system is designed to say that the information was not found rather than inventing an answer.

---

# 👁️ Multimodal Industrial Intelligence

Industrial information is not always text.

The Workbench supports a vision workflow for:

- Inspection images
- Engineering diagrams
- Process diagrams
- Scanned material
- Visual evidence

Example:

```text
Engineering Image
       ↓
Local Vision Model
       ↓
Visual Interpretation
       ↓
Structured Findings
       ↓
Local AI Response
```

The prototype has been tested with an engineering process-flow image.

For industrial drawings, the system is intentionally conservative about uncertain visual details and can report limitations instead of fabricating unreadable labels or symbols.

---

# 🛠️ Tool Execution

The Workbench can route suitable tasks to controlled local tools.

Example:

```text
User Request
     ↓
Task = Code / Calculation
     ↓
Local Python Execution
     ↓
Result
     ↓
Response
```

Example request:

```text
Calculate the average of 10, 20, 30 and 40.
```

Result:

```text
25.0
```

For production deployment, code execution should be strengthened with:

- Container isolation
- CPU limits
- Memory limits
- Execution timeouts
- Filesystem restrictions
- Network restrictions
- Process restrictions
- Allowlisted libraries / operations

---

# 📝 Inspection Review Workflow

The current prototype includes an inspection-review workflow.

```text
Inspection Request
       ↓
Retrieve relevant knowledge
       ↓
Local LLM analysis
       ↓
Review Note Generation
       ↓
DOCX Artifact
       ↓
Employee History
```

Generated artifacts can be stored locally for controlled access.

---

# 🔐 Authentication & Role-Based Access Control

The current UI includes separate Administrator and Employee workflows.

```text
                 ┌───────────────┐
                 │ Role Selection│
                 └───────┬───────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Administrator            Employee
              │                     │
              ▼                     ▼
        Admin Login            Employee Login
              │                     │
              ▼                     ▼
        Admin Workspace        Employee Workspace
```

### Administrator capabilities

- 👥 Employee management
- 🔑 Permission management
- 📚 Knowledge-base management
- 📊 Dashboard information
- 📝 System administration workflows

### Employee capabilities

- 🤖 AI Workbench
- 📜 Personal history
- 👤 Profile
- 🔐 Permission-aware access

---

# 👥 Employee Management

Administrators can create employee accounts with:

- Employee ID
- Name
- Email
- Department
- Designation
- AI permission
- Document permission
- Reports permission
- Code-execution permission
- Sensitive-document permission

Employee records support controlled activation and status management.

---

# 🧾 Employee History & Auditability

The system stores employee request history using the employee identity as the access boundary.

Stored information includes:

- Employee ID
- Request
- Task type
- Response
- Source-document information
- Execution status
- Artifact path
- Timestamp

Employee history queries are filtered by the authenticated employee identity so an employee workspace is intended to expose that employee's own history.

---

# 🗄️ Authentication Database

The prototype uses a local SQLite authentication database.

```text
data/auth/auth.db
```

Main tables include:

```text
admins
employees
employee_history
```

Passwords are stored using password hashing rather than plaintext storage.

> Local authentication data is intentionally excluded from the public repository through `.gitignore`.

---

# 📚 Admin Knowledge Management

The Admin Panel includes knowledge-base management for controlled internal content.

The workflow supports:

```text
Administrator
     ↓
Upload Document
     ↓
Document Metadata
     ↓
Processing
     ↓
Chunking
     ↓
Knowledge Store
     ↓
Retrieval
```

Metadata can include:

- Category
- Department
- Equipment
- Description
- Version
- Document status

The knowledge-management layer is designed so future production versions can add document version history, approval workflows, richer search, and stronger archival controls.

---

# 🧪 Current Prototype Capabilities

| Capability | Prototype Status |
|---|---|
| Local text LLM inference | ✅ Implemented |
| Ollama integration | ✅ Implemented |
| Mistral local inference | ✅ Implemented |
| Local vision workflow | ✅ Implemented |
| LLaVA image analysis | ✅ Implemented |
| Local RAG | ✅ Implemented |
| MRPL document demonstration | ✅ Implemented |
| Task classification | ✅ Implemented |
| Controlled Python execution workflow | ✅ Implemented |
| Inspection review note | ✅ Implemented |
| DOCX artifact generation | ✅ Implemented |
| Admin authentication | ✅ Implemented |
| Employee authentication | ✅ Implemented |
| Employee management | ✅ Implemented |
| Permission management | ✅ Implemented |
| Employee history | ✅ Implemented |
| Admin knowledge management | ✅ Implemented |
| Multi-agent industrial investigation | 🔄 Extension |
| SQL/data agent | 🔄 Extension |
| Advanced analytics agent | 🔄 Extension |
| Production-grade sandbox isolation | 🔄 Extension |
| Production identity integration | 🔄 Extension |
| Network egress verification | 🔄 Deployment task |

---

# 🧱 Project Structure

```text
sovereign_ai/
│
├── app/
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── employee_management.py
│   │   └── panel.py
│   │
│   ├── agent/
│   │   └── orchestrator.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── history.py
│   │   ├── service.py
│   │   ├── session.py
│   │   └── ui.py
│   │
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── database.py
│   │   ├── ingestion.py
│   │   ├── processor.py
│   │   └── service.py
│   │
│   ├── models/
│   │   └── ollama_client.py
│   │
│   └── ui.py
│
├── rag/
│   └── retriever.py
│
├── data/
│   ├── auth/
│   ├── input/
│   ├── knowledge/
│   ├── output/
│   └── corpus/
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

> Local data, authentication databases, generated outputs, and other development artifacts are excluded from Git where appropriate.

---

# ⚙️ Technology Stack

## AI / LLM

- Python
- Ollama
- Mistral
- LLaVA
- Open-weight local models
- Agent orchestration

## Retrieval / Knowledge

- PyMuPDF
- TF-IDF
- Cosine similarity
- Section-aware chunking
- Local document processing

## Application

- Streamlit
- Python modules
- SQLite authentication database

## Data / Backend

- PostgreSQL
- SQLite
- Pandas
- NumPy

## APIs / Development

- FastAPI
- REST APIs
- Git
- GitHub

## Document / Artifact Generation

- python-docx

---

# 🖥️ Hardware Demonstration Environment

The prototype has been tested in a college GPU environment using:

```text
GPU:
NVIDIA A100-PCIE-40GB

VRAM:
40 GB

Python:
3.12.x

CUDA-enabled PyTorch:
Available

Ollama:
Local model serving
```

The architecture is intended to scale according to the organization's available compute infrastructure.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Vignesh14007/sovereign-ai.git
cd sovereign-ai
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
```

## 3. Activate it

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Install and run Ollama

Install Ollama according to your operating system and ensure the local Ollama service is available.

Example model setup:

```bash
ollama pull mistral
ollama pull llava
```

The exact model names can be changed according to the deployment environment.

---

# ▶️ Run the Application

From the project root:

```bash
PYTHONPATH="$PWD" streamlit run app/ui.py
```

The Streamlit interface will provide the authentication flow and route the user to the appropriate workspace.

---

# 🔑 Prototype Authentication

The development environment may contain locally created prototype accounts.

**Do not reuse development credentials in production.**

For a real deployment:

- Change all initial passwords
- Use strong password policies
- Add rate limiting
- Add account lockout
- Integrate organization identity where appropriate
- Use secure secret storage
- Add one-time activation tokens
- Centralize audit logging

Authentication data is intentionally kept outside the Git repository.

---

# 🧪 Validation Examples

### Local RAG

```text
Question
   ↓
Retriever
   ↓
Top relevant sections
   ↓
Mistral
   ↓
Evidence-grounded answer
```

### Code task

```text
Task:
Calculate the average of 10, 20, 30 and 40.

Execution:
Local Python

Result:
25.0
```

### Vision task

```text
Engineering drawing
       ↓
LLaVA
       ↓
Structured visual interpretation
       ↓
Industrial response
```

### Inspection workflow

```text
Inspection request
       ↓
Knowledge retrieval
       ↓
Local LLM analysis
       ↓
Review note
       ↓
DOCX output
```

---

# 🛡️ Security Principles

The project follows these design principles:

### 1. Local-first AI

Use local models instead of requiring external AI inference APIs.

### 2. Least privilege

Users should receive only the capabilities and documents authorized for their role.

### 3. Controlled tools

The AI should not automatically receive unrestricted access to the operating system.

### 4. Evidence-based responses

RAG responses should be grounded in retrieved evidence.

### 5. Auditability

Important user operations should be traceable.

### 6. Separation of user data

Employee history should be scoped to the authenticated employee.

### 7. No secrets in Git

Credentials, `.env` files, local databases, generated outputs, and local data are excluded from the public repository.

---

# ⚠️ Production Security Requirements

This repository is a **prototype / hackathon implementation**, not a production-certified industrial security platform.

Before deployment in a real industrial environment, additional controls should be implemented and validated, including:

- Enterprise identity and SSO
- MFA
- Network segmentation
- Firewall and egress restrictions
- Containerized tool execution
- OS-level sandboxing
- Resource quotas
- Secure secret management
- Encryption at rest and in transit
- Centralized audit logging
- Security monitoring
- Vulnerability scanning
- Model provenance and integrity checks
- Document access policies
- Data retention policies
- Backup and disaster recovery
- Human approval gates for consequential actions

---

# 🔬 Domain Adaptation Strategy

The platform is designed around three complementary layers:

```text
                 Domain Adaptation
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
 Prompt / Task       Local RAG      LoRA / QLoRA
 Specialization      Grounding      Fine-tuning
```

The prototype primarily demonstrates:

1. Task/prompt specialization
2. Local document grounding through RAG

Parameter-efficient fine-tuning can be introduced when authorized domain-specific training examples are available.

The prototype does **not** claim to have been fine-tuned on confidential MRPL data.

---

# 🧭 Development Roadmap

## Phase 1 — Foundation

- [x] Local LLM inference
- [x] Streamlit application
- [x] Basic orchestrator
- [x] Local model integration

## Phase 2 — Knowledge Intelligence

- [x] PDF processing
- [x] Section-aware chunking
- [x] Local RAG
- [x] MRPL document demonstration
- [x] Knowledge management foundation

## Phase 3 — Security

- [x] Administrator authentication
- [x] Employee authentication
- [x] Role separation
- [x] Permission management
- [x] Employee history
- [ ] Enterprise SSO
- [ ] MFA
- [ ] One-time activation tokens
- [ ] Central audit infrastructure

## Phase 4 — Agentic Intelligence

- [x] Task classification
- [x] Capability routing
- [x] Local tool execution workflow
- [ ] Dedicated data agent
- [ ] Dedicated analytics agent
- [ ] Dedicated knowledge agent
- [ ] Dedicated verification agent
- [ ] Multi-step planning

## Phase 5 — Multimodal Intelligence

- [x] Local vision model
- [x] Image analysis
- [x] Engineering drawing demonstration
- [ ] OCR pipeline
- [ ] Scanned-document understanding
- [ ] Multimodal evidence correlation

## Phase 6 — Industrial Workbench

- [ ] SQL agent
- [ ] Time-series analytics
- [ ] Anomaly detection
- [ ] Industrial charts
- [ ] Cross-source evidence correlation
- [ ] Structured report generation
- [ ] PPT / Excel generation
- [ ] Verification layer

## Phase 7 — Production Hardening

- [ ] Container sandbox
- [ ] Network egress controls
- [ ] Enterprise identity
- [ ] Centralized logging
- [ ] Security monitoring
- [ ] Model governance
- [ ] Deployment automation

---

# 🏆 Intended Final Workflow

The long-term workflow is:

```text
                         USER
                           │
                           ▼
                  Authentication / RBAC
                           │
                           ▼
                  Natural Language Query
                           │
                           ▼
                  Task Understanding
                           │
                           ▼
                    Task Planning
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Data Agent   Knowledge     Vision Agent
             │           Agent            │
             ▼             ▼             ▼
        SQL / Time     Local RAG       Images /
        Series Data    Documents       Drawings
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Evidence Fusion
                           │
                           ▼
                      Verification
                           │
                           ▼
                    Local LLM Response
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Answer       Artifact       Audit
                           │
                           ▼
                       User
```

---

# ⭐ Key Value Proposition

> **Sovereign AI Workbench is designed to move industrial AI from simple question-answering toward controlled, evidence-driven investigation using locally hosted AI, authorized enterprise knowledge, tools, and multimodal evidence.**

The key architectural idea is:

```text
Understand
   ↓
Plan
   ↓
Retrieve
   ↓
Query
   ↓
Analyze
   ↓
Correlate
   ↓
Verify
   ↓
Generate
   ↓
Audit
```

---

# 👨‍💻 Project Team

### Team ALGNITE

Built as a Smart India Hackathon 2026 project for:

**SIH26117 — Mangalore Refinery and Petrochemicals Limited (MRPL)**

**Theme:** Smart Automation  
**Category:** Software

---

# 📌 Repository

**GitHub:**  
https://github.com/Vignesh14007/sovereign-ai

---

# 📄 Disclaimer

This repository represents a **hackathon / research prototype**.

It demonstrates architectural concepts and working prototype capabilities using local/open-weight models and publicly available or synthetic demonstration data.

It should not be interpreted as a production-certified industrial control, safety, cybersecurity, or decision-making system.

Any deployment involving real industrial data should be performed only with appropriate organizational authorization, security controls, validation, and human oversight.

---

# ⭐ Project Vision

The long-term vision is to build a **controlled industrial AI workbench** where engineers can ask complex questions in natural language and receive evidence-backed assistance across structured data, documents, images, and analytical tools — while keeping sensitive information within the organization's approved computing environment.

**Sovereign AI Workbench — Understand industrial data. Investigate with AI. Keep control of the data.**
