from app.llm import get_summarization_response
from app.utils.logging_server import setup_logger

logger = setup_logger("Summarization")

def get_summary_from_llm(query: str) -> str:
    """Summarizes a given user text.
    """
    logger.info(f"Summarizing user query: {query[:50]}...")
    return get_summarization_response(query)
