from fastapi import FastAPI
from pydantic import BaseModel
from rag_agent.rag_chain import build_rag_chain

app = FastAPI()
rag_chain = build_rag_chain()

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    print("Received query:", request.message)
    result = rag_chain(request.message)
    print("RAG result:", result)
    answer = result["result"]
    print("RAG answer:", answer)
    return QueryResponse(response=answer)  