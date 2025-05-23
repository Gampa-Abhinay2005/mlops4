from prefect import flow, task

from app.services.retrieval import get_retrieval_from_llm, retrieve_relevant_info


@task
def chat_analysis(text: str) -> str:
    return retrieve_relevant_info(text)

@flow
def chat_flow(query: str) -> str:
    return chat_analysis(query)

@task
def retrival_analysis(text: str) -> str:
    return get_retrieval_from_llm(text)

@flow
def retrival_flow(query: str) -> str:
    return retrival_analysis(query)
