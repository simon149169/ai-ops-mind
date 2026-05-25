```markdown
# AI Ops Mind - Intelligent Operations Assistant Platform v2.0
* **中文版本**：`README_ZH.md` 
* **英文版本**：`README.md`
> **Product Positioning**: A closed-loop AI AIOps platform built for production environments. Proactively senses alerts, intelligently analyzes root causes, generates reliable reports, and automatically retains knowledge, shifting operations from "firefighting mode" to "preventative mode."

## 💡 Core Features

### 🚨 Proactive Alert Ingestion
* **Webhook Gateway**: Supports standard alert webhooks from Prometheus AlertManager, DingTalk, Lark, etc.
* **Automated Triage Engine**: Smart routing based on severity levels (P0/P1/P2/P3).
* **Idempotency & Deduplication**: Utilizes Redis TTL mechanisms to suppress alert storms.
* **Scheduled Inspection Scheduling**: Built-in automated inspection jobs to uncover hidden risks proactively.

### 🔍 Intelligent Analysis Engine
* **Log Root Cause Analysis (RCA)**: Deeply mines massive logs to locate the first scene of a failure rapidly.
* **Multi-Service Multi-Dimensional Correlation**: Spans across microservice call chains to trace fault propagation paths.
* **Alert Aggregation & Noise Reduction**: Converges fragmented, scattered alerts into a single cohesive incident.
* **Confidence Scoring**: Provides High/Medium/Low confidence scores to support human operator decision-making.

### 📋 RCA Report Generation
* **Auto-Triggered Generation**: Automatically starts analysis and drafting when critical alerts fire.
* **Timeline Sequencing**: Accurately maps out anomalous changes and events before and after the incident.
* **Source Citations & References**: Explicitly references raw log snippets or metrics to ensure trustworthiness.
* **Markdown Export**: Perfectly compatible with major collaboration platforms for easy sharing and archiving.

### 📚 Closed-Loop Knowledge Base
* **Historical Case Retrieval (RAG)**: Matches similar past outages using Retrieval-Augmented Generation technology.
* **Automated Knowledge Accumulation**: Automatically transforms verified analysis results into long-term knowledge assets.
* **Expert Feedback & Alignment**: Allows SRE experts to score and correct AI results, facilitating continuous model improvement.
* **Knowledge Version Control**: Manages iterations of knowledge entries to guarantee accuracy and timeliness.

### 💬 Interaction & Notification Layer
* **SSE Streaming Chat**: Provides an ultra-smooth, typewriter-style LLM chat interaction experience.
* **Multi-Turn Context Memory**: Supports deep follow-up questions for continuous fault troubleshooting.
* **Human-in-the-Loop Approval**: Enforces manual approval flows for high-risk remedial actions to protect production.
* **IM Notifications**: Deeply integrated with DingTalk and Lark for real-time alerting throughout the incident lifecycle.

---

## 🏗️ Technical Architecture

┌─────────────────────────────────────────────────────────────┐
│                       Frontend                              │
│    HTML + CSS + JavaScript (Dark Theme)                     │
├─────────────────────────────────────────────────────────────┤
│                     API Gateway                             │
│    FastAPI (Routing / JWT / Rate Limiting / SSE)            │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                            │
│    Chat / Log Analyzer / Alert Diagnoser / RCA Generator    │
│    Triage Engine / Webhook Handler / Notifier               │
├─────────────────────────────────────────────────────────────┤
│                       AI Layer                              │
│    LLM Adapter / RAG Engine / Prompt Manager                │
│    Confidence Scorer                                        │
├─────────────────────────────────────────────────────────────┤
│                      Data Layer                             │
│    ChromaDB (Vector) / SQLite/PG (Relational) / Redis (Queue)│
└─────────────────────────────────────────────────────────────┘


### 🛠️ Tech Stack Selection

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML + CSS + JavaScript | Modern dark-themed dashboard, lightweight, and embeddable. |
| **Backend** | FastAPI (Python 3.11+) | Native asynchronous support, high-concurrency, built-in SSE, auto-generated OpenAPI docs. |
| **LLM** | OpenAI-compatible API | Pluggable architecture supporting OpenAI, DeepSeek, Qwen, Ollama, etc. |
| **Vector DB** | ChromaDB | Zero-configuration, embedded vector database powering RAG capability. |
| **Database** | SQLite / PostgreSQL | Persists user sessions, historical incident metadata, and knowledge records. |
| **Queue/Cache** | Redis | Asynchronous alert message queues, rate limiting, and idempotency deduplication. |
| **Scheduler** | APScheduler | Powers periodic cron inspections and background platform health checks. |
| **Deployment** | Docker + K8s | Standardized container images, supporting production-grade horizontal scaling. |

---

## 🚀 Quick Start

### Prerequisites

* Python 3.11+
* Redis 7.0+
* Docker & Docker Compose (Optional)

### 1. Install Dependencies

```bash
cd ai-ops-mind
pip install -r requirements.txt
2. Configure Environment Variables
Bash
cp .env.example .env
# Edit .env file to configure your LLM API Keys, Database, and Redis connections
3. Launch the Server
Option 1: Run directly (Development Mode)

Bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Option 2: Using Makefile

Bash
make run
Option 3: Using Docker Compose (Recommended for Production/Staging)

Bash
docker-compose up -d
4. Access Services
API Documentation: http://localhost:8000/docs

Frontend UI Dashboard: http://localhost:8000/static/index.html

Health Check Endpoint: http://localhost:8000/api/health

Prometheus Metrics: http://localhost:8000/api/metrics

<img width="1515" height="1247" alt="image" src="https://github.com/user-attachments/assets/50def48e-d0d9-45d7-9ad0-3477da03427e" />
<img width="2362" height="1157" alt="image" src="https://github.com/user-attachments/assets/717c0b83-0942-40ec-8bc0-7f915f375fa3" />



🔌 API Endpoints Reference
Method	Path	Description
POST	/api/webhook/alert	Ingests incoming alerts pushed from external systems (Prometheus, etc.)
POST	/api/chat/stream	Multi-turn SSE streaming interactive dialogue with the AI assistant
POST	/api/analyze	Submits raw application logs for smart anomaly and root-cause analysis
POST	/api/alert	Triggers alert correlation and aggregated diagnostic procedures
POST	/api/rca	Manually or automatically generates structured Markdown RCA reports
POST	/api/feedback	Submits validation feedback or corrective scoring from SRE experts
POST	/api/knowledge/upload	Uploads operational manuals or historical autopsy documents into the RAG vector store
GET	/api/knowledge/search	Test endpoint for querying knowledge via RAG vector search
GET	/api/metrics	Exposes standard system and business metrics for Prometheus scraping
GET	/api/health	Returns service health status
📁 Project Structure
ai-ops-mind/
├── app/                    # Backend application core
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # App settings and environment loader
│   ├── api/               # API route definitions (RESTful & SSE)
│   ├── services/          # Core business services (RAG, Diagnostics, Report Gen)
│   ├── prompts/           # LLM Prompt templates and pipeline management
│   ├── models/            # Relational models (SQLAlchemy) & schemas (Pydantic)
│   └── utils/             # Helper utilities (crypto, time, formatting)
├── frontend/              # Static frontend assets
│   ├── index.html         # Main workspace HTML
│   ├── css/               # UI Stylesheets (Dark Theme)
│   └── js/                # Core JS logic handling SSE and UI updates
├── knowledge/             # Pre-loaded raw data for RAG
│   ├── cases/             # Post-mortem incident case studies (Markdown/JSON)
│   └── docs/              # Standard Operating Procedures (SOPs) & handbooks
├── k8s/                    # Kubernetes production deployment manifests
├── tests/                 # Unit and integration test suites
├── docker-compose.yml     # Multi-container multi-service orchestration setup
├── Dockerfile             # Docker image generation script for the backend
├── Makefile               # Shortcuts for frequent development commands
└── requirements.txt       # Python packages and runtime dependencies
⚙️ Core Configuration Guide
LLM Provider Settings
Configure your LLM backend in the .env file. It supports any API compatible with the OpenAI specification:

代码段
# Option 1: DeepSeek (Recommended for Production)
OPENAI_API_BASE=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
OPENAI_MODEL_NAME=deepseek-chat
OPENAI_API_KEY=your-deepseek-api-key

# Option 2: OpenAI
OPENAI_API_BASE=[https://api.openai.com/v1](https://api.openai.com/v1)
OPENAI_MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your-openai-api-key

# Option 3: Local Deployment via Ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL_NAME=qwen:7b-chat
OPENAI_API_KEY=not-needed-for-local
Security Gateway Verification
To prevent unauthorized webhook requests, it is highly recommended to enable HMAC-SHA256 signature checking:

代码段
WEBHOOK_SECRET=your-custom-secure-webhook-secret-key
💡 Usage Examples
1. Mocking Proactive Alert Ingestion
Bash
curl -X POST http://localhost:8000/api/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{
    "alert_id": "test-alert-001",
    "severity": "P0",
    "service": "payment-service",
    "title": "HighErrorRate",
    "description": "Error rate exceeded 300% in the last 5 minutes",
    "fired_at": "2026-05-25T03:14:20Z"
  }'
2. Requesting Raw Log Diagnostics
Bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"logs": "🪲 ERROR [payment-service] [2026-05-25 03:14:22] Connection refused to mysql:3306 at pool.py:145"}'
3. Querying Similar Cases from Knowledge Base
Bash
curl "http://localhost:8000/api/knowledge/search?query=mysql%20connection%20refused"
📊 Observability & Metrics
The platform exposes standard Prometheus metrics via /api/metrics, allowing seamless integration with Grafana dashboards:

Metric Name	Type	Description
ops_llm_requests_total	Counter	Total number of LLM API requests executed.
ops_llm_latency_seconds	Histogram	Latency distribution of LLM calls in seconds.
ops_rag_hit_rate	Gauge	Effective hit rate of RAG knowledge retrieval.
ops_webhook_received_total	Counter	Total number of external alert webhooks processed.
ops_analysis_confidence	Gauge	Distribution of AI diagnostic confidence levels.
ops_feedback_correct_rate	Gauge	AI analysis accuracy trend validated by SRE experts.
🛡️ License
This project is open-sourced under the MIT License.

AI Ops Mind - Smartening Operations, Stabilizing Production 🚀
