from app.llm import evaluate_micro_skills
from app.utils.logging_server import setup_logger

logger = setup_logger("MicroSkillAssessment")

def evaluate_skills(agent_response: str) -> str:
    logger.info(f"Evaluating micro-skills for response: {agent_response[:50]}...")
    return evaluate_micro_skills(agent_response)
