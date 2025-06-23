from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from rag_agent.rag_chain import build_rag_chain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Employee Teams RAG API",
    description="Local RAG pipeline for employee data queries",
    version="1.0.0"
)

# Add CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global RAG chain instance
rag_chain = None

class QueryRequest(BaseModel):
    message: str
    include_sources: Optional[bool] = False

class QueryResponse(BaseModel):
    response: str
    sources: Optional[list] = None
    confidence: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    ollama_available: bool
    faiss_index_loaded: bool
    total_employees: Optional[int] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG chain on startup"""
    global rag_chain
    try:
        rag_chain = build_rag_chain()
        logger.info("RAG chain initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG chain: {e}")
        raise

@app.get("/")
async def root():
    """Serve the web frontend"""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Employee Teams RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "stats": "/stats",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check if Ollama is running
        import requests
        ollama_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_available = ollama_response.status_code == 200
    except:
        ollama_available = False
    
    # Check if FAISS index is loaded
    faiss_index_loaded = rag_chain is not None
    
    # Get employee count if possible
    total_employees = None
    if rag_chain:
        try:
            # This is a simple way to get document count - you might need to adjust
            total_employees = len(rag_chain.retriever.vectorstore.index_to_docstore_id)
        except:
            pass
    
    return HealthResponse(
        status="healthy" if (ollama_available and faiss_index_loaded) else "degraded",
        ollama_available=ollama_available,
        faiss_index_loaded=faiss_index_loaded,
        total_employees=total_employees
    )

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """Main query endpoint with enhanced error handling"""
    if not rag_chain:
        raise HTTPException(status_code=503, detail="RAG chain not initialized")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty")
    
    try:
        logger.info(f"Processing query: {request.message}")
        
        # Process the query
        result = rag_chain.invoke({"question": request.message})
        
        # Extract response and metadata
        answer = result.get("result", "No answer found")
        sources = result.get("source_documents", []) if request.include_sources else None
        
        # Calculate confidence (simple heuristic based on source relevance)
        confidence = None
        if sources:
            # Simple confidence based on number of relevant sources
            confidence = min(1.0, len(sources) * 0.3)
        
        logger.info(f"Query processed successfully. Answer length: {len(answer)}")
        
        return QueryResponse(
            response=answer,
            sources=sources,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process query: {str(e)}"
        )

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        if not rag_chain:
            return {"error": "RAG chain not available"}
        
        # Get basic stats
        stats = {
            "total_documents": len(rag_chain.retriever.vectorstore.index_to_docstore_id),
            "embedding_model": "phi3",
            "llm_model": "phi3"
        }
        
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")  