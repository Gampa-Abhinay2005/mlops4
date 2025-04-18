from app.llm import get_response_template
from app.utils.logging_server import setup_logger

logger = setup_logger("ResponseTemplate")

def suggest_response_template(user_query: str) -> str:
    logger.info(f"Suggesting response template for query: {user_query[:50]}...")
    return get_response_template(user_query)
