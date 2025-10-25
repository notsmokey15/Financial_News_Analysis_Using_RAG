from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from .config import GROQ_API_KEY
from .rag_core import query_documents

# Initialize FastAPI app
app = FastAPI(
    title="Financial News Analyst AI",
    description="An API to chat with the latest financial news using RAG and Groq."
)

# Initialize the Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Pydantic model for the request body to ensure data is in the correct format
class QueryRequest(BaseModel):
    question: str

@app.post("/query-news")
async def handle_query(request: QueryRequest):
    """
    Handles user queries by retrieving relevant news and generating a response with Groq.
    """
    if not request.question:
        raise HTTPException(status_code=400, detail="Question field cannot be empty.")

    # 1. Retrieve relevant documents from the vector database (RAG part)
    relevant_docs = query_documents(request.question)
    
    if not relevant_docs:
        return {"answer": "I couldn't find any relevant news articles to answer your question. Try ingesting some data first."}

    # 2. Combine the documents into a single context string
    context = "\n\n---\n\n".join(relevant_docs)

    # 3. Create a prompt for the LLM
    prompt = f"""
    You are a professional financial analyst. Your task is to answer the user's question based *only* on the provided news context.
    If the context does not contain the answer, state that clearly. Do not use any external knowledge.

    CONTEXT:
    {context}

    USER'S QUESTION:
    {request.question}

    ANSWER:
    """

    try:
        # 4. Send the prompt to the Groq API for a fast response
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            # This is the updated, currently active model from Groq's production list
            model="llama-3.1-8b-instant",
        )
        answer = chat_completion.choices[0].message.content
        return {"answer": answer, "sources": relevant_docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred with the Groq API: {e}")

@app.get("/")
def read_root():
    return {"status": "Financial News Analyst AI is running."}
