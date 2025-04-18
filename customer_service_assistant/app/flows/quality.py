from prefect import flow, task

from app.services.quality import assess_quality


@task
def quality_analysis(agent_response: str, policy: str = None) -> str:
    return assess_quality(agent_response,policy)

@flow
def quality_flow(query: str) -> str:
    return quality_analysis(query)
