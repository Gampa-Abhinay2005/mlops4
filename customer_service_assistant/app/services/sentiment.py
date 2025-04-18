from app.llm import get_sentiment_response
from app.utils.logging_server import setup_logger

logger = setup_logger("SentimentAnalysis")

def analyze_sentiment(user_query: str) -> str:
    """Analyzes the sentiment of the given user query.
    """
    logger.info(f"Analyzing sentiment for query: {user_query[:50]}...")

    prompt = f"Analyze the sentiment of the following text: {user_query}"
    sentiment = get_sentiment_response(prompt)
    logger.debug(f"Sentiment analysis result: {sentiment}")
    return sentiment
