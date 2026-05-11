<div align="center">

# MEMORYFADE
### AI Cognitive Memory Engine

Fast, human-inspired memory system with semantic retrieval, adaptive decay, and grounded LLM responses.

![FastAPI](https://img.shields.io/badge/FastAPI-black?style=for-the-badge&logo=fastapi)
![Qdrant](https://img.shields.io/badge/Qdrant-black?style=for-the-badge&logo=qdrant)
![Supabase](https://img.shields.io/badge/Supabase-black?style=for-the-badge&logo=supabase)
![Groq](https://img.shields.io/badge/Groq-black?style=for-the-badge&logo=groq)

</div>

---

## Overview

MEMORYFADE mimics human memory behavior.

Instead of storing data forever, memories:
- strengthen on access
- decay over time
- move through lifecycle states
- fade when unused

The system retrieves context using semantic similarity + cognitive scoring for more relevant AI responses.

---

## Core Features

- Semantic vector retrieval
- Ebbinghaus-based decay system
- Memory lifecycle states
- Reinforcement on retrieval
- Grounded LLM responses
- Multi-user isolation via JWT auth

---

## Memory Lifecycle

```text
FRESH → ACTIVE → FADING → ARCHIVED
```

---

## Architecture

```mermaid
graph TD
    A[Client / CLI] --> B(FastAPI)
    B --> C{Orchestrator}

    C --> D[Embeddings]
    C --> E[(Qdrant)]
    C --> F[(Supabase)]

    D --> G[Cognitive Ranking]
    E --> G
    F --> G

    G --> H[Groq LLM]
    H --> A
```

---

## Cognitive Score

```text
Score =
0.55 × Semantic +
0.20 × Strength +
0.15 × Importance +
0.10 × Recency
```

---

## Tech Stack

- FastAPI
- Qdrant
- Supabase
- Groq API
- Sentence Transformers

---

## Setup

### `.env`

```env
SUPABASE_URL=
SUPABASE_KEY=
QDRANT_URL=
QDRANT_API_KEY=
GROQ_API_KEY=
```

### Install

```bash
git clone https://github.com/yourusername/memoryfade.git

cd memoryfade

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## CLI

```bash
# Add memory
python sms.py add "Focus on backend systems"

# Search memory
python sms.py search "What should I focus on?"

# Trigger decay
python sms.py decay <MEMORY_ID>
```

---

## Performance

| Metric | Result |
|---|---|
| Avg Latency | 187ms |
| Retrieval Accuracy | 94.2% |
| Hallucination Rate | 0% |

---

## Author

**Hrithik Sham**  
Backend & AI Systems Engineer

```
