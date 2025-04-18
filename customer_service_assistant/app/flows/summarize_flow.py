from prefect import flow, task
from app.services.summarization import get_summary_from_llm

@task
def summarize_text(text: str) -> str:
    return get_summary_from_llm(text)

@flow
def summarize_flow(query: str) -> str:
    return summarize_text(query)
