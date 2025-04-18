from app.llm import get_intent_response
from app.utils.logging_server import setup_logger

logger = setup_logger("IntentDetection")

def get_intent_from_llm(user_query: str) -> str:
    """
    Determines the intent behind a user query.
    """
    logger.info(f"Getting intent for query: {user_query[:50]}...")
    return get_intent_response(user_query)
