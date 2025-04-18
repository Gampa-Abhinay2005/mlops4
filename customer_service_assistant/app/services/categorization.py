from app.llm import categorize_conversation
from app.utils.logging_server import setup_logger

logger = setup_logger("ConversationCategorization")

def categorize(user_conversation: str) -> str:
    logger.info("Categorizing conversation...")
    return categorize_conversation(user_conversation)
