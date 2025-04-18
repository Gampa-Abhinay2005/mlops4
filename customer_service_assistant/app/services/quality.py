from app.llm import evaluate_response_quality
from app.utils.logging_server import setup_logger

logger = setup_logger("QualityAssurance")

def assess_quality(agent_response: str, policy: str = None) -> str:
    policy = policy or "The agent must be polite and courteous to the customer."
    logger.info(f"Evaluating agent response: {agent_response[:50]}...")
    return evaluate_response_quality(agent_response, policy)
