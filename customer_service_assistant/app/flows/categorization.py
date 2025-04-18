from prefect import flow, task
from app.services.categorization import categorize
@task
def categorize_analysis(text: str) -> str:
    return categorize(text)

@flow
def categorize_flow(query: str) -> str:
    return categorize_analysis(query)
