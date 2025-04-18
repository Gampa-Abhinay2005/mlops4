from prefect import flow, task
from app.services.ticket import create_ticket
@task
def ticket_analysis() -> str:
    return create_ticket()

@flow
def ticket_flow(query: str) -> str:
    return ticket_analysis()
