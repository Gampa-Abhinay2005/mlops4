from prefect import flow, task
from app.services.intent import get_intent_from_llm

@task
def intent_analysis(text: str) -> str:
    return get_intent_from_llm(text)

@flow
def intent_flow(query: str) -> str:
    return intent_analysis(query)
