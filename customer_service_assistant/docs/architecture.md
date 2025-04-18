# 🏗️ System Architecture

## 🧠 Overview

The **Customer Service Assistant** is a modular, AI-powered platform built to enhance customer support by providing intelligent automation, seamless transcription, and real-time insights to both customers and agents. The system supports audio and text interactions, with ML-powered analysis, retrieval, summarization, and ticketing workflows orchestrated by **Prefect** and tracked with **MLflow**.

---

## 🧩 Components

### 1. User Interfaces
- **Customer Chat UI**: Enables real-time conversation using Streamlit with integrated retrieval and summarization.
- **Agent Dashboard**: Presents conversations, AI context (sentiment, summary), suggested responses, and quality metrics.

### 2. Backend Services
- **Message Router**: Central component routing messages to different analysis engines.
- **LLM Engine**: Handles NLP tasks using **Ollama’s LLaMA 3**, such as:
  - Intent Detection
  - Sentiment Analysis
  - Response Suggestion
  - Summarization
- **Knowledge Base Retriever**: Retrieves markdown documents relevant to the conversation from a local repository.

### 3. Workflow Orchestration
- **Prefect Workflows**: Orchestrates complex tasks like summarization, ticket creation, categorization, and skill evaluation.

### 4. Monitoring & Logging
- **MLflow**:
  - Tracks each flow execution (e.g., transcription, summarization)
  - Logs metrics like transcript length, intent types, sentiment ratios
  - Stores artifacts like conversation logs and generated summaries

### 5. Containerized Services
- At least two microservices are **Dockerized** (e.g., transcription, summarization) to ensure modularity and scalability.

---

## 🧬 Mermaid Architecture Diagram

```mermaid
graph TD
  A[Customer UI] -->|Sends Message| B[Message Router]
  A2[Agent UI] -->|Receives/Replies| B
  A3[Transcription UI] -->|Uploads Audio| B
  B --> C[LLM Engine]
  B --> D[Knowledge Retriever]
  B --> M[Audio Processing Engine]
  C --> F1[Sentiment Analysis]
  C --> F2[Intent Detection]
  C --> F3[Response Suggestion]
  C --> F4[Summarization]
  D --> G[Markdown Documents]
  M --> N1[Whisper Transcription]
  M --> N2[Speaker Segmentation]
  M --> N3[Role Detection]
  B --> I[Prefect Workflows]
  I --> J1[Ticket Creation]
  I --> J2[Quality Checks]
  I --> J3[Conversation Categorization]
  I --> J4[Micro-Skill Evaluation]
  I --> K[Docker Services]
  B --> L[MLflow Logging]

  subgraph Frontend
    A
    A2
    A3
  end

  subgraph Backend
    B
    C
    D
    M
    I
    K
    L
  end

  subgraph Storage
    G
    H
  end
