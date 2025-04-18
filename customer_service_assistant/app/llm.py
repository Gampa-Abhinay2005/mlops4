import subprocess

import ollama

from app.utils.config_loader import load_toml_config
from app.utils.logging_server import setup_logger

# Load config
config = load_toml_config("app_config.toml")["llm"]
logger = setup_logger("LLM")

llm_model = config["model"]
temperature = config["temperature"]
top_p = config["top_p"]

def query_ollama(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", llm_model, prompt],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Ollama subprocess failed: {e.stderr}")
        return "Sorry, something went wrong with the LLM."
    except Exception as e:
        logger.error(f"Unexpected error: {e!s}")
        return "Sorry, something went wrong with the LLM."

def get_sentiment_response(query: str):
    logger.info(f"Getting sentiment for query: {query}")
    prompt = f"Analyze the sentiment of this text and return one of [Positive, Negative, Neutral] and give a short discription : {query}"
    return query_ollama(prompt)

def get_retrieval_response(query: str):
    logger.info(f"Retrieving information for query: {query}")
    prompt = f"Retrieve relevant factual information or answer concisely for: {query}"
    return query_ollama(prompt)

def get_summarization_response(query: str):
    logger.info(f"Summarizing content for query: {query}")
    prompt = f"Summarize the following text: {query}"
    return query_ollama(prompt)

def get_intent_response(query: str):
    logger.info(f"Determining intent for query: {query}")
    prompt = f"What is the user's intent behind this message: {query}"
    return query_ollama(prompt)

def get_solution_suggestion(query: str) -> str:
    prompt = f'Based on past resolved cases, suggest a potential solution for the following issue:\n"{query}"'
    return query_ollama(prompt)

def get_response_template(query: str) -> str:
    prompt = f'Suggest a professional response template for the following customer question:\n"{query}"'
    return query_ollama(prompt)

def get_ticket_creation_response() -> str:
    return "New ticket needs to be created."

def evaluate_response_quality(agent_response: str, policy: str = "The agent must be polite and courteous to the customer.") -> str:
    prompt = f'Evaluate the following agent response based on the policy: "{policy}"\n\nResponse:\n{agent_response}'
    return query_ollama(prompt)

def categorize_conversation(conversation: str) -> str:
    prompt = f"Categorize this conversation into one of the following categories: Billing, Technical Issue, General Inquiry, Complaint, Feedback.\nConversation:\n{conversation}"
    return query_ollama(prompt)

def evaluate_micro_skills(agent_response: str) -> str:
    prompt = f"Evaluate the following agent response on clarity, politeness, empathy, and helpfulness. Provide feedback for each.\n\nResponse:\n{agent_response}"
    return query_ollama(prompt)

def ask_llama3(prompt: str) -> str:
    """Queries the LLaMA 3 model via the Ollama API and returns the response.
    
    Args:
        prompt (str): The prompt/question to send to the model.
    
    Returns:
        str: The model's response.

    """
    try:
        # Send the prompt to the LLaMA 3 model using the Ollama API
        response = ollama.chat(
            model="llama3",  # Ensure you are using the correct model name
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        # Extract and return the content from the response
        return response["message"]["content"]
    except Exception as e:
        # Handle any errors that occur during the API call
        return f"An error occurred while querying LLaMA 3: {e!s}"
