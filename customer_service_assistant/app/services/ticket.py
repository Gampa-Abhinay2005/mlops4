from app.llm import get_ticket_creation_response
from app.utils.logging_server import setup_logger

logger = setup_logger("TicketCreation")

def create_ticket() -> str:
    logger.info("Triggering ticket creation...")
    return get_ticket_creation_response()
