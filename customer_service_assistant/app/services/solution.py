from app.llm import get_solution_suggestion
from app.utils.logging_server import setup_logger

logger = setup_logger("SolutionSuggestion")

def suggest_solution(user_query: str) -> str:
    logger.info(f"Suggesting solution for query: {user_query[:50]}...")
    return get_solution_suggestion(user_query)
