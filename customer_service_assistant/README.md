# Customer Service Assistant


A modular AI-powered assistant for customer service that transcribes audio, identifies speakers, classifies roles (agent/customer), and logs everything with MLflow. It uses **Prefect workflows** to orchestrate tasks and **Docker** for containerized services.

---

## 🚀 Features

- ✅ Audio Transcription using `faster-whisper`
- 🎤 Speaker Diarization (basic, alternating speakers)
- 🧠 Role Identification (Agent vs Customer) using keyword heuristics
- 📊 MLflow Logging of:
  - Parameters
  - Metrics (e.g., word counts, segment count)
  - Artifacts (transcripts, speaker maps)
- ⚙️ Prefect Workflows for managing pipelines
- 🐳 Dockerized components for modular deployment
- 📝 Frontend interface for file upload and result viewing

---

## 🧱 Architecture

```mermaid
graph TD
  A[Customer UI] -->|Upload Audio| B[FastAPI API]
  B --> C[Prefect Flow: Transcribe]
  C --> D[Whisper Transcriber]
  C --> E[Speaker Diarizer]
  C --> F[Role Identifier]
  C --> G[MLflow Logger]
  G --> H[mlruns/]
  B --> I[Response with Transcript + Speakers]

  subgraph Services
    B
    C
    D
    E
    F
    G
  end
