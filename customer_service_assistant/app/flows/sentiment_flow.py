from prefect import flow, task
from app.services.sentiment import analyze_sentiment

@task
def sentiment_analysis(text: str) -> str:
    return analyze_sentiment(text)

@flow
def sentiment_flow(query: str) -> str:
    return sentiment_analysis(query)
