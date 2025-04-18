# Customer Service Assistant 🧠🎧📞

## 🔍 Project Overview

The **Customer Service Assistant** is a full-stack AI-driven tool to assist customer support workflows using natural language processing and speech technologies. It processes user queries via **text** or **audio**, uses **LLMs (via Ollama)** for reasoning, and supports real-time **agent augmentation**.

---

## ⚙️ Key Features

### 🧩 Modular Architecture
- **FastAPI**: REST backend with all functionality exposed via endpoints.
- **Streamlit UI**: Real-time frontend for both customers and agents.
- **Whisper (FasterWhisper)**: Transcribes audio to text.
- **Speaker Diarization**: Alternates speakers and detects roles using keyword patterns.
- **Prefect Workflows**: Orchestrates all steps like summarization, transcription, intent detection, etc.
- **MLflow Logging**: Logs copious and structured metadata, metrics, and artifacts.
- **Dockerization**: Services like transcription and summarization containerized for reproducibility.

---

## 🧪 Technical Stack

- **Language**: Python 3.11  
- **LLMs**: Ollama (llama3)  
- **Libraries**: FastAPI, Prefect, MLflow, Streamlit, FasterWhisper  
- **Tools**: Docker, Just, Uvicorn, Httpx, Loguru

---

## 📦 Functional Highlights

- 🎙️ **Audio Transcription**: Converts uploaded `.wav`/`.mp3` files to structured transcript.
- 🧠 **Intent Detection**: Detects user's query intent using local LLMs.
- 📚 **Retrieval**: Retrieves relevant information from a markdown-based KB.
- 📊 **Sentiment & Summarization**: Assesses emotion and provides compressed context.
- 🧑‍💻 **Agent Panel**:
  - View conversation summary
  - Sentiment insights
  - Suggested response templates
  - Solution suggestions
  - Micro-skill evaluations
  - Ticket creation

---

## 🚀 Deployment

- Two services (e.g. transcription and summarization) run as **Dockerized microservices**.
- `mlflow_logger.py` handles experiment tracking with local or remote MLflow server.
- `prefect` handles pipeline orchestration, logging, and execution.
- Easy-to-use `justfile` for local testing and container execution.

---
