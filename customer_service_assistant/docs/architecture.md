# System Architecture

## Overview

The Customer Service Assistant is a modular AI-powered platform designed to enhance customer support interactions. It integrates real-time chat interfaces with intelligent features like sentiment analysis, knowledge retrieval, and automated summarization to assist both customers and agents effectively.

## Components

### 1. User Interfaces
- *Customer Chat UI*: A straightforward interface allowing customers to send messages.
- *Agent Dashboard*: Displays ongoing conversations alongside AI-driven suggestions and relevant information.

### 2. Backend Services
- *Message Router*: Manages the flow of messages between users and backend processes.
- *LLM Engine*: Performs tasks such as intent detection, sentiment analysis, and response generation using language models.
- *Knowledge Base Retriever*: Fetches pertinent documents from a repository based on conversation context.

### 3. Workflow Orchestration
- *Prefect Workflows*: Automates tasks like summarization (/summarize), ticket creation (/newticket), and quality checks based on triggers.

### 4. Monitoring and Logging
- *MLflow*: Tracks performance metrics, logs workflow executions, and monitors agent interactions for continuous improvement.

### 5. Containerized Services
- *Dockerized Modules*: Certain services, such as document processing or summarization, are encapsulated in Docker containers for scalability and isolation.
```mermaid
graph TD
  A[Customer UI] -->|Sends Message| B[Message Router]
  A2[Agent UI] -->|Receives/Replies| B
  B --> C[LLM Engine]
  B --> D[Knowledge Base Retriever]
  B --> E[Transcript Memory]
  C --> F1[Sentiment Analysis]
  C --> F2[Intent Detection]
  C --> F3[Response Suggestion]
  C --> F4[Summarization]
  D --> G[Markdown Documents]
  E --> H[Past Transcripts]
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
  end

  subgraph Backend
    B
    C
    D
    E
    I
    K
    L
  end

  subgraph Storage
    G
    H
  end