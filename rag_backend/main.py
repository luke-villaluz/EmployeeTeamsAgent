from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    # For now, just echo the message back
    return QueryResponse(response=f"You said: {request.message}")