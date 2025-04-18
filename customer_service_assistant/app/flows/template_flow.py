from prefect import flow, task

from app.services.response_template import suggest_response_template


@task
def template_analysis(text: str) -> str:
    return suggest_response_template(text)

@flow
def template_flow(query: str) -> str:
    return template_analysis(query)
