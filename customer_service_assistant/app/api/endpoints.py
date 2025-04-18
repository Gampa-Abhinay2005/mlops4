# app/main.py

from fastapi import FastAPI,UploadFile, File
from pydantic import BaseModel

from app.flows.summarize_flow import summarize_flow
from app.flows.sentiment_flow import sentiment_flow
from app.flows.intent_flow import intent_flow
from app.flows.template_flow import template_flow
from app.flows.transcription import transcribe_flow
from app.flows.retrieval import retrival_flow,chat_flow
from app.flows.quality import quality_flow
from app.flows.categorization import categorize_flow
from app.flows.micro_skills import evaluate_flow
from app.flows.solution_flow import solution_flow
from app.flows.ticket import ticket_flow

app = FastAPI()

# Define a request model for user input
class UserQuery(BaseModel):
    query: str

@app.post("/intent")
def get_intent(user_query: UserQuery):
    """
    Endpoint to detect intent from user query.
    """
    intent = intent_flow(user_query.query)
    return {"intent": intent}

@app.post("/retrieve")
def retrieve_info(user_query: UserQuery):
    """
    Endpoint to retrieve relevant information based on user query.
    """
    information = retrival_flow(user_query.query)
    return {"information": information}

@app.post("/sentiment")
def get_sentiment(user_query: UserQuery):
    """
    Endpoint to analyze sentiment of the user query.
    """
    sentiment = sentiment_flow(user_query.query)
    return {"sentiment": sentiment}

@app.post("/summarize")
def summarize_text_endpoint(user_query: UserQuery):
    """
    Endpoint to summarize a given user text.
    """
    summary = summarize_flow(user_query.query)
    return {"summary": summary}

@app.post("/solution")
def get_solution(user_query: UserQuery):
    """
    Endpoint to suggest a solution based on user query.
    """
    return {"solution": solution_flow(user_query.query)}

@app.post("/response-template")
def get_template(user_query: UserQuery):
    """
    Endpoint to suggest a response template based on user query.
    """
    return {"template": template_flow(user_query.query)}

@app.post("/newticket")
def new_ticket():
    """
    Endpoint to create a new ticket based on user query.
    """
    return {"message": ticket_flow()}

class AgentInput(BaseModel):
    response: str
    policy: str = None

@app.post("/quality")
def check_quality(agent_input: AgentInput):
    """
    Endpoint to assess the quality of an agent's response based on a policy.
    """
    return {"evaluation": quality_flow(agent_input.response, agent_input.policy)}

@app.post("/categorize")
def categorize_convo(user_query: UserQuery):
    """
    Endpoint to categorize a conversation based on user query.
    """
    return {"category": categorize_flow(user_query.query)}

@app.post("/micro-skills")
def micro_skills(agent_input: AgentInput):
    """
    Endpoint to evaluate micro-skills of an agent's response.
    """
    return {"skills_feedback": evaluate_flow(agent_input.response)}

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    result = await transcribe_flow(contents, file.filename)
    return result
class ChatMessage(BaseModel):
    query: str

@app.post("/chat")
async def chat(message: ChatMessage):
    """
    Endpoint to handle customer queries and retrieve relevant information.
    
    Args:
        message (dict): A dictionary containing the customer message.
        
    Returns:
        dict: A dictionary containing the response to be sent to the customer.
    """
    response = chat_flow(message.query)
    return {"chat": response}
