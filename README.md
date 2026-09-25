# 🏭 SOVEREIGN AI WORKBENCH

### 🔐 An On-Premise Agentic Multimodal AI Platform for Confidential Industrial Intelligence

<p align="center">

<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/LLM-Mistral-FF7000?style=for-the-badge" />
<img src="https://img.shields.io/badge/Runtime-Ollama-black?style=for-the-badge" />
<img src="https://img.shields.io/badge/AI-RAG-8A2BE2?style=for-the-badge" />
<img src="https://img.shields.io/badge/AI-Agentic%20AI-6A5ACD?style=for-the-badge" />
<img src="https://img.shields.io/badge/Deployment-On--Premise-2E8B57?style=for-the-badge" />

</p>

<p align="center">
<strong>Natural Language → Agentic Orchestration → Enterprise Knowledge → Evidence → Local AI Reasoning</strong>
</p>

---

## 🧠 Overview

**Sovereign AI Workbench** is an **on-premise agentic multimodal AI platform** designed for confidential industrial intelligence.

Industrial organizations generate large volumes of heterogeneous information across:

- 📊 Sensor and time-series data
- 🗄️ SQL databases
- 🔧 Maintenance records
- 📘 Standard Operating Procedures (SOPs)
- 📚 Technical manuals
- 📄 Inspection reports
- 🖼️ Machine and inspection images
- 📝 Operational logs
- ⚠️ Historical failure records
- 🏭 Engineering and annual reports

The challenge is not simply storing this information. The challenge is enabling engineers and operators to **query, retrieve, analyze, and reason across these different sources through a unified natural-language interface**.

For example:

> **"Why did Compressor C-204 show abnormal behavior last week?"**

Answering such a question may require retrieving operational information, identifying abnormal trends, checking historical failures, reviewing maintenance records, searching technical documentation, and examining inspection information.

Sovereign AI Workbench provides an AI-driven architecture for coordinating these workflows while supporting an **on-premise-first deployment model**.

---

# 🎯 Problem Statement

Industrial intelligence is often fragmented across disconnected systems.

A typical investigation may require:

```text
Sensor / Time-Series Data
          +
SQL Databases
          +
Maintenance Records
          +
SOPs & Technical Manuals
          +
Inspection Reports
          +
Machine Images
          +
Historical Failure Data
          ↓
   Manual Investigation
```

This creates several challenges:

- 🔀 Information is distributed across different systems.
- 🔎 Engineers must manually search multiple sources.
- 🔗 Structured and unstructured data are difficult to use together.
- 🕐 Historical context can take time to retrieve.
- 📚 Technical documentation is disconnected from operational information.
- 🤖 Conventional chat interfaces do not inherently coordinate multiple enterprise tools.
- 🔐 Confidential industrial information may require strict data-governance boundaries.

---

# 💡 Proposed Solution

Sovereign AI Workbench introduces an **agentic intelligence layer** between the user and enterprise information sources.

```text
                         👤 USER
                           │
                           ▼
                  💬 Natural Language Query
                           │
                           ▼
                🧠 Intent / Domain Classifier
                           │
                           ▼
                  🤖 Agent Orchestrator
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      📚 RAG          📄 File Tools     🛠️ AI Tools
     Retrieval         & Analysis       & Services
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🔎 Evidence Collection
                           │
                           ▼
                   🧠 Local LLM
                           │
                           ▼
                 💬 Contextual Answer
                           │
                           ▼
                    🔐 Audit Layer
```

The platform is built around three core principles:

### 🔐 Sovereignty
Sensitive industrial information can remain within the organization's controlled infrastructure.

### 🤖 Agentic Reasoning
The system can classify requests, determine appropriate processing paths, and coordinate available tools.

### 🌐 Multimodal Intelligence
The architecture is designed to work across documents, structured information, operational data, and visual inspection information.

---

# 🚀 Core Capabilities

## 🤖 Agentic AI

The platform uses an agent-oriented architecture instead of treating every request as a simple question-answering task.

The agent layer contains components for:

- 🧠 Domain classification
- 🎯 Intent identification
- 🔄 Request orchestration
- 🛠️ Tool selection
- ⚙️ Tool execution
- 🔎 Evidence retrieval
- 💬 Response generation
- 🔐 Audit logging

This provides a foundation for multi-step industrial reasoning.

---

## 📚 Retrieval-Augmented Generation

The RAG pipeline retrieves relevant information before generating a response.

```text
📄 Industrial Documents
          │
          ▼
   📥 Document Processing
          │
          ▼
      🧹 Cleaning
          │
          ▼
      ✂️ Chunking
          │
          ▼
   🔍 Filtering
          │
          ▼
 📚 Knowledge Corpus
          │
          ▼
    🔎 Retriever
          │
          ▼
  📌 Relevant Context
          │
          ▼
      🧠 Local LLM
          │
          ▼
   💬 Grounded Response
```

The repository contains components for:

- Document processing
- Chunk generation
- Data cleaning
- Chunk filtering
- Retrieval
- Question answering
- Knowledge-corpus preparation

---

# 🖼️ Multimodal Industrial Intelligence

Industrial information is not limited to text.

The platform is designed to work across multiple information modalities:

| Modality | Example |
|---|---|
| 📄 Documents | Technical reports, SOPs |
| 📊 Structured Data | Operational measurements |
| 🗄️ Databases | Enterprise records |
| 🖼️ Images | Inspection images |
| 🔧 Maintenance Data | Maintenance history |
| ⚠️ Failure Data | Historical failures |
| 📝 Logs | Operational events |

This architecture provides a foundation for combining textual, structured, and visual evidence.

---

# 🧠 Local LLM Execution

The platform is designed around **local LLM execution using Ollama-compatible workflows**.

This allows model inference to operate within the controlled environment rather than requiring every confidential request to be sent to an external AI API.

```text
🏭 Industrial Environment
          │
          ▼
   🔐 Sovereign AI
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
   📚 RAG     🧠 Local LLM
    │           │
    └─────┬─────┘
          ▼
     💬 Response
```

The project also contains model-training and dataset-preparation workflows for domain-specific AI development.

---

# 🛠️ Tool-Based Architecture

The platform separates capabilities into reusable tools.

Current tool components include:

- 📄 File reading
- 📝 Document generation
- 🧩 Tool registration
- 🔒 Sandboxed execution
- 🔐 Audit operations

This architecture allows additional capabilities to be introduced as modular tools.

---

# 🔄 Agentic Workflow

A typical request follows this architecture:

```text
👤 User Question
       │
       ▼
🧠 Intent / Domain Classification
       │
       ▼
🤖 Agent Orchestrator
       │
       ├──────────────────┐
       │                  │
       ▼                  ▼
📚 RAG Retrieval      🛠️ Tool Selection
       │                  │
       │                  ▼
       │             ⚙️ Tool Execution
       │                  │
       └─────────┬────────┘
                 ▼
        🔎 Evidence Collection
                 │
                 ▼
            🧠 Local LLM
                 │
                 ▼
          💬 Final Response
                 │
                 ▼
            🔐 Audit Log
```

---

# 🏭 Example Industrial Investigation

### User Query

```text
Why did Compressor C-204 show abnormal behavior last week?
```

The agentic workflow can conceptually perform:

```text
1️⃣ Identify the equipment
       ↓
2️⃣ Determine the relevant time period
       ↓
3️⃣ Retrieve operational information
       ↓
4️⃣ Analyze abnormal trends
       ↓
5️⃣ Search historical failures
       ↓
6️⃣ Retrieve maintenance records
       ↓
7️⃣ Search technical documentation
       ↓
8️⃣ Review available inspection information
       ↓
9️⃣ Combine the retrieved evidence
       ↓
🔟 Generate a contextual explanation
```

The target transformation is:

```text
❌ MANUAL INVESTIGATION

Database
   ↓
Reports
   ↓
Maintenance Records
   ↓
SOPs
   ↓
Inspection Records
   ↓
Historical Failures
   ↓
Manual Analysis
```

into:

```text
✅ AGENTIC INVESTIGATION

Natural Language Question
          ↓
     AI Orchestration
          ↓
   Multiple Data Sources
          ↓
    Evidence Retrieval
          ↓
      Local Reasoning
          ↓
   Contextual Industrial Insight
```

---

# 🧩 Project Architecture

```text
sovereign_ai/
│
├── 📁 app/
│   │
│   ├── 🤖 agent/
│   │   ├── classifier.py
│   │   ├── domain.py
│   │   └── orchestrator.py
│   │
│   ├── 🔌 api/
│   │
│   ├── 🔐 security/
│   │   └── audit.py
│   │
│   ├── 🛠️ tools/
│   │   ├── document_generator.py
│   │   ├── file_reader.py
│   │   ├── registry.py
│   │   └── sandbox/
│   │       └── executor.py
│   │
│   └── 🖥️ ui.py
│
├── 📚 rag/
│   ├── documents/
│   ├── qa.py
│   └── retriever.py
│
├── 🧪 training/
│   ├── build_chunks.py
│   ├── build_sft_dataset.py
│   └── clean_chunks.py
│
├── 🧪 test_mistral_mrpl.py
├── 🧠 train_mistral_mrpl.py
├── 🖥️ ui.py
├── 📦 requirements.txt
├── 🔒 .gitignore
└── 📖 README.md
```

---

# 🧱 Main Components

## `app/agent/`

Contains the agentic reasoning layer.

### `classifier.py`
Handles classification of incoming requests and helps determine the appropriate domain or processing path.

### `domain.py`
Contains domain-oriented definitions used by the agent system.

### `orchestrator.py`
Coordinates the agent workflow and connects requests with appropriate processing components and tools.

---

## `app/tools/`

Contains reusable system capabilities.

### `file_reader.py`
Provides file and document reading functionality.

### `document_generator.py`
Provides document-generation functionality.

### `registry.py`
Provides registration and management of available tools.

### `sandbox/executor.py`
Provides controlled execution functionality for operations requiring an execution environment.

---

## `app/security/`

Contains security and traceability components.

### `audit.py`
Provides audit-oriented functionality for tracking system activity.

---

## `rag/`

Contains the Retrieval-Augmented Generation pipeline.

### `retriever.py`
Handles retrieval of relevant information from the prepared knowledge base.

### `qa.py`
Connects retrieved information with question-answering workflows.

---

## `training/`

Contains data preparation workflows for domain-specific model development.

The training pipeline supports:

- Dataset construction
- Chunk generation
- Data cleaning
- Training-data preparation

---

# 🧪 Model Training Workflow

The project contains workflows for preparing and training domain-specific data.

```text
🏭 Industrial Domain Data
          │
          ▼
📥 Dataset Construction
          │
          ▼
🧹 Data Cleaning
          │
          ▼
✂️ Chunk / Sample Preparation
          │
          ▼
📚 Training Dataset
          │
          ▼
🧠 Model Training
          │
          ▼
🧪 Evaluation
          │
          ▼
🧠 Local Domain Model
```

Training-related components include:

```text
train_mistral_mrpl.py
test_mistral_mrpl.py
training/build_sft_dataset.py
training/build_chunks.py
training/clean_chunks.py
```

Training and inference are treated as separate workloads because their compute requirements can differ significantly.

---

# 🔐 Security & Data Privacy

Security is a core consideration because industrial AI systems may process confidential information.

The platform follows an **on-premise-first architecture**.

```text
🏭 Industrial Data
        │
        ▼
🔐 Organization-Controlled Infrastructure
        │
        ▼
🤖 Sovereign AI Workbench
        │
   ┌────┼────┐
   ▼    ▼    ▼
  RAG  Tools Local LLM
   │    │    │
   └────┼────┘
        ▼
   💬 AI Response
```

The project contains security-oriented components for:

- 🔐 Audit logging
- 🛡️ Controlled tool execution
- 📦 Sandboxed execution
- 🧩 Tool registration
- 🏠 Local processing

### Important

This repository represents a prototype/workbench. Production deployment requires additional:

- Authentication
- Authorization
- Role-Based Access Control
- Network isolation
- Secrets management
- Monitoring
- Threat modeling
- Security testing
- Compliance validation

---

# 🗂️ Data Handling

The public repository intentionally does **not** include the project's local industrial data directory.

Sensitive or environment-specific content should remain outside the public repository, including:

- 📄 Confidential industrial documents
- 📊 Private datasets
- 🖼️ Inspection records
- 🔑 Credentials
- 🔐 API keys
- 🧠 Local model weights
- 📝 Environment-specific configuration
- 🖥️ Server-specific files

The `.gitignore` configuration prevents local project data, logs, model files, archives, and secrets from being committed accidentally.

---

# ⚙️ Technology Stack

| Layer | Technology |
|---|---|
| 🐍 Language | Python |
| 🧠 LLM | Mistral |
| 🏠 Local Runtime | Ollama |
| 🤖 AI Architecture | Agentic AI |
| 📚 Knowledge Retrieval | RAG |
| 📄 Document Processing | Python |
| 🧪 Model Training | Mistral Training Workflow |
| 🖥️ Interface | Python UI |
| 🔐 Security | Audit + Controlled Execution |
| 🌐 Version Control | Git |
| ☁️ Repository | GitHub |
| 🏭 Deployment Model | On-Premise |

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Vignesh14007/sovereign-ai.git
cd sovereign-ai
```

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🧠 Local LLM Setup

The project uses an Ollama-compatible local LLM workflow.

Install Ollama from:

https://ollama.com/

Verify the installation:

```bash
ollama --version
```

Pull the required model:

```bash
ollama pull mistral
```

Verify:

```bash
ollama list
```

---

# ▶️ Running the Application

The project contains the main UI entry point:

```text
ui.py
```

If the configured interface uses Streamlit:

```bash
streamlit run ui.py
```

The exact execution command may depend on the current application configuration.

---

# 📚 RAG Workflow

The repository contains document-processing workflows for preparing the retrieval corpus.

Typical workflow:

```text
📄 Source Documents
       │
       ▼
🧩 build_chunks.py
       │
       ▼
🧹 clean_chunks.py
       │
       ▼
🔍 Filtering / Preparation
       │
       ▼
📚 Knowledge Corpus
       │
       ▼
🔎 retriever.py
       │
       ▼
💬 qa.py
       │
       ▼
🧠 LLM Response
```

---

# 🧪 Training Workflow

Domain-specific training workflows are separated from the runtime application.

```text
Domain Data
    ↓
Dataset Construction
    ↓
Cleaning
    ↓
Training Dataset
    ↓
Model Training
    ↓
Evaluation
    ↓
Local Model
```

Relevant scripts:

```text
train_mistral_mrpl.py
test_mistral_mrpl.py
training/build_sft_dataset.py
training/build_chunks.py
training/clean_chunks.py
```

---

# 🔬 Development Approach

The platform is designed as a modular AI workbench rather than a single-purpose chatbot.

```text
              🧠 REASONING
                   │
                   ▼
              🤖 AGENTS
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
        📚 RAG   🛠️ TOOLS  📊 DATA
          │        │        │
          └────────┼────────┘
                   ▼
              🏠 LOCAL LLM
                   │
                   ▼
              🔐 SECURITY
                   │
                   ▼
                💬 UI
```

This separation allows individual components to evolve independently.

---

# 📈 Current Scope

The current workbench establishes a foundation for:

- 🤖 Agent-based request routing
- 🧠 Domain classification
- 🔄 Tool orchestration
- 🏠 Local LLM interaction
- 📚 Retrieval-Augmented Generation
- 📄 Industrial document processing
- 🧪 Domain-specific training workflows
- 📁 File and document interaction
- 🔒 Controlled tool execution
- 🔐 Audit-oriented operations
- 🏭 On-premise deployment

---

# 🔮 Future Development

## 🗄️ Enterprise Data Connectors

Extend the agent layer to interact with:

- SQL databases
- Time-series databases
- Industrial historians
- Maintenance management systems
- Operational data platforms

---

## 🖼️ Advanced Multimodal Reasoning

Extend multimodal capabilities with:

- Machine inspection images
- Visual anomaly analysis
- OCR
- Technical diagrams
- Image-text reasoning

---

## 🤖 Advanced Agent Planning

Extend the orchestrator toward multi-step planning:

```text
User Question
      ↓
Planning
      ↓
Tool Selection
      ↓
Multiple Tool Calls
      ↓
Evidence Validation
      ↓
Reasoning
      ↓
Final Answer
```

---

## 🔐 Enterprise Access Control

Future enterprise capabilities can include:

- User authentication
- Role-Based Access Control
- Permission-aware retrieval
- Department-level access
- Tool-level authorization

---

## 📊 Observability

Potential monitoring capabilities:

- Agent traces
- Tool execution traces
- Retrieval metrics
- Model latency
- Error monitoring
- Resource utilization
- Evaluation metrics

---

# 🏭 Target Enterprise Architecture

```text
                         👤 USER
                           │
                           ▼
                  🔐 Authentication
                           │
                           ▼
                  🤖 Agent Orchestrator
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       📚 RAG          🗄️ Data Tools     🛠️ AI Tools
          │                │                │
          ▼                ▼                ▼
   Knowledge Base     Enterprise DBs     Local LLM
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    🔎 Evidence Layer
                           │
                           ▼
                    🧠 AI Reasoning
                           │
                           ▼
                    💬 Final Response
                           │
                           ▼
                    🔐 Audit Layer
```

---

# 🎯 Project Objective

The long-term objective of Sovereign AI Workbench is to provide a unified industrial intelligence layer where users can interact with complex enterprise information using natural language.

Instead of requiring engineers to manually navigate multiple systems:

```text
Database
   ↓
Reports
   ↓
Maintenance Records
   ↓
SOPs
   ↓
Inspection Records
   ↓
Historical Failures
   ↓
Manual Analysis
```

the target workflow is:

```text
Natural Language Question
          ↓
   Agentic Investigation
          ↓
  Multiple Enterprise Sources
          ↓
     Evidence Retrieval
          ↓
     Local AI Reasoning
          ↓
 Contextual Industrial Insight
```

---

# ⚠️ Limitations

This repository represents an active prototype/workbench rather than a production-certified industrial platform.

Important limitations include:

- Production-grade access control requires additional implementation.
- Industrial cybersecurity requires infrastructure-level controls beyond the application.
- AI-generated responses require appropriate validation before operational decisions.
- Model performance depends on the quality and coverage of available knowledge.
- Retrieval quality depends on document processing and indexing.
- Training and inference requirements depend on the selected model and available hardware.
- Production deployment requires additional monitoring, testing, fault tolerance, and security validation.

The platform should therefore be evaluated against the organization's operational, security, and compliance requirements before production use.

---

# 📁 Repository Structure

```text
sovereign-ai/
│
├── 📁 app/
│   ├── 🤖 agent/
│   │   ├── classifier.py
│   │   ├── domain.py
│   │   └── orchestrator.py
│   │
│   ├── 🔌 api/
│   │
│   ├── 🔐 security/
│   │   └── audit.py
│   │
│   ├── 🛠️ tools/
│   │   ├── document_generator.py
│   │   ├── file_reader.py
│   │   ├── registry.py
│   │   └── sandbox/
│   │       └── executor.py
│   │
│   └── 🖥️ ui.py
│
├── 📁 rag/
│   ├── documents/
│   ├── qa.py
│   └── retriever.py
│
├── 📁 training/
│   ├── build_chunks.py
│   ├── build_sft_dataset.py
│   └── clean_chunks.py
│
├── 🧪 test_mistral_mrpl.py
├── 🧠 train_mistral_mrpl.py
├── 🖥️ ui.py
├── 📦 requirements.txt
├── 🔒 .gitignore
└── 📖 README.md
```

---

# 🤝 Development Principles

The project follows these engineering principles:

### 🧩 Modular Architecture
Separate agents, tools, retrieval, security, training, and interface components.

### 🔐 Secure Data Handling
Keep sensitive industrial data and credentials outside the public source repository.

### 🏠 Local-First AI
Support local model inference and retrieval for controlled environments.

### 🛠️ Extensible Tools
Add new capabilities as modular tools instead of coupling everything to one workflow.

### 📚 Evidence-Oriented Responses
Use retrieval to provide relevant context before response generation.

### 🔎 Traceability
Maintain audit-oriented components for system activity and tool execution.

### 🧪 Reproducibility
Keep data preparation and training workflows structured and repeatable.

---

# 📌 Project Information

| Field | Details |
|---|---|
| 🏷️ Project | Sovereign AI Workbench |
| 📋 Problem Statement | SIH26117 |
| 🏭 Organization | Mangalore Refinery and Petrochemicals Limited (MRPL) |
| 💻 Category | Software |
| 🎯 Theme | Smart Automation |
| 🧠 Architecture | Agentic Multimodal AI |
| 🏠 Deployment | On-Premise |
| 📚 Retrieval | RAG |
| 🧠 Local LLM | Mistral + Ollama |
| 🐍 Language | Python |

---

# 🛡️ Data & Security Notice

This public repository contains the **software implementation and development workflows**.

Private industrial documents, local datasets, credentials, model files, and environment-specific files are intentionally excluded from version control.

Do not commit confidential enterprise information, API keys, passwords, private certificates, or production credentials to this repository.

---

<p align="center">

### 🏭 Sovereign AI Workbench

<strong>Agentic AI • RAG • Multimodal Intelligence • Local LLM • On-Premise AI</strong>

</p>
