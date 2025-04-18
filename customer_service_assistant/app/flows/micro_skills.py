from prefect import flow, task

from app.services.micro_skills import evaluate_skills


@task
def evalute_analysis(text: str) -> str:
    return evaluate_skills(text)

@flow
def evaluate_flow(query: str) -> str:
    return evalute_analysis(query)
