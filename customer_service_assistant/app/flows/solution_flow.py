from prefect import flow, task
from app.services.solution import suggest_solution

@task
def solution_analysis(text: str) -> str:
    return suggest_solution(text)

@flow
def solution_flow(query: str) -> str:
    return solution_analysis(query)
