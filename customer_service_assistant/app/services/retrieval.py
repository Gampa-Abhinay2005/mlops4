from pathlib import Path

from app.llm import ask_llama3, get_retrieval_response
from app.utils.logging_server import setup_logger

logger = setup_logger("ContextAwareRetrieval")
KNOWLEDGE_BASE_DIR = Path("knowledge_base")

def get_retrieval_from_llm(user_query: str) -> str:
    """Retrieves relevant information based on user query.
    """
    logger.info(f"Retrieving information for query: {user_query[:50]}...")
    return get_retrieval_response(user_query)


def semantic_search(query: str) -> str:
    """Perform semantic search using LLaMA 3 to find the most relevant knowledge base section.
    """
    # Step 1: Ask LLaMA to choose the topic
    topics = ["billing", "shipping", "returns", "payments", "subscriptions", "technical_support", "account", "cancellation", "security"]
    topic_list = ", ".join(topics)
    prompt = f"Customer's query: '{query}'.\n\nHere are the topics: {topic_list}.\n\nWhich topic is most relevant to the query? Answer with only the topic name."

    topic = ask_llama3(prompt).lower().strip()

    # Step 2: Load corresponding file
    file_path = KNOWLEDGE_BASE_DIR / f"{topic}.md"
    if not file_path.exists():
        return "Sorry, I couldn't find relevant information."

    with open(file_path, encoding="utf-8") as file:
        full_content = file.read()

    # Step 3: Ask LLaMA to extract only the most relevant section from the file
    refine_prompt = f"""
A customer asked: "{query}"

Here is a document from our knowledge base about {topic}:

--- DOCUMENT START ---
{full_content}
--- DOCUMENT END ---

Please extract only the most relevant section or paragraph that answers the customer's query clearly.
"""

    answer = ask_llama3(refine_prompt)
    return answer.strip()

def retrieve_relevant_info(message: str) -> str:
    """Retrieve relevant knowledge base information and log the interaction.
    
    Args:
        message (str): The customer query.
    
    Returns:
        str: Relevant information or an error message.

    """
    logger.info(f"Customer query: {message}")
    relevant_info = semantic_search(message)
    logger.info(f"Retrieved information: {relevant_info}")
    return relevant_info
