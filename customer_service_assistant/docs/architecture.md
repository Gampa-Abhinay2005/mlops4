```mermaid
graph TD
    Customer -->|sends message| FastAPI
    FastAPI --> LLM
    LLM -->|retrieves| Markdown_KB
    LLM -->|searches| Past_Transcripts
    FastAPI --> Agent_UI
```