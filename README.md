# Employee Teams RAG Agent

A local, secure, AI-powered employee information assistant using Retrieval-Augmented Generation (RAG) with Ollama, FAISS, and LangChain.

## 🚀 Features

- **🔒 100% Local** - No cloud services, no credit cards, no external dependencies
- **🤖 AI-Powered** - Uses Ollama for local LLM inference and embeddings
- **📊 Excel Integration** - Direct processing of employee Excel data
- **🔍 Advanced Queries** - Natural language queries with structured data analysis
- **🌐 Web Interface** - Beautiful, modern web frontend for easy testing
- **📈 Health Monitoring** - Real-time system health and statistics
- **🧪 Comprehensive Testing** - Full test suite for reliability
- **⚙️ Configuration Management** - Flexible configuration system

## 🏗️ Architecture

```
Employee Teams Agent/
├── rag_backend/           # Python FastAPI backend
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration management
│   ├── static/           # Web frontend
│   └── rag_agent/        # RAG pipeline components
│       ├── embed_store.py    # FAISS vector store
│       ├── load_excel.py     # Excel data loader
│       ├── rag_chain.py      # RAG chain implementation
│       └── advanced_queries.py # Advanced query capabilities
├── teams-bot/            # Teams bot (future integration)
├── data/                 # Excel files
├── tests/                # Test suite
└── requirements.txt      # Python dependencies
```

## 🛠️ Installation

### Prerequisites

1. **Python 3.8+**
2. **Node.js 18+** (for Teams bot)
3. **Ollama** - [Install Ollama](https://ollama.ai/)

### Setup

1. **Clone and setup environment:**
```bash
git clone <your-repo>
cd Employee-Teams-Agent
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Install Ollama model:**
```bash
ollama pull phi3
```

3. **Prepare your data:**
   - Place your employee Excel file in `data/employees.xlsx`
   - Ensure it has columns: Name, Title, Department, Email, Start Date, etc.

4. **Generate embeddings:**
```bash
cd rag_backend
python -m rag_agent.embed_store
```

## 🚀 Usage

### Start the Backend

1. **Start Ollama:**
```bash
ollama serve
```

2. **Start the FastAPI backend:**
```bash
cd rag_backend
uvicorn main:app --reload
```

3. **Access the web interface:**
   - Open http://localhost:8000 in your browser
   - Or use the API directly at http://localhost:8000/docs

### API Endpoints

- **`GET /`** - Web frontend
- **`GET /health`** - System health check
- **`GET /stats`** - System statistics
- **`POST /query`** - Main query endpoint
- **`GET /docs`** - Interactive API documentation

### Example Queries

```bash
# Basic query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is the CTO?"}'

# Query with sources
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "Who is the CTO?", "include_sources": true}'

# Health check
curl "http://localhost:8000/health"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `rag_backend/` directory:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3

# Data Configuration
EXCEL_DATA_PATH=../data/employees.xlsx

# API Configuration
HOST=127.0.0.1
PORT=8000

# RAG Configuration
RAG_K=4
RAG_CHAIN_TYPE=stuff
```

### Configuration Validation

```bash
cd rag_backend
python config.py
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_rag_backend.py -v

# Run with coverage
pytest tests/ --cov=rag_backend --cov-report=html
```

### Test Categories

- **Unit Tests** - Individual component testing
- **Integration Tests** - End-to-end workflow testing
- **Performance Tests** - Response time and load testing
- **Security Tests** - Input validation and CORS testing

## 📊 Advanced Features

### Advanced Query Engine

The system includes an advanced query engine with capabilities for:

- **Department Analysis** - Employee counts, role distribution
- **Seniority Analysis** - Experience-based categorization
- **Natural Language Parsing** - Extract structured queries from natural language
- **Experience Filtering** - Search by years of experience
- **Company Overview** - Comprehensive organizational statistics

### Example Advanced Queries

```python
from rag_backend.rag_agent.advanced_queries import EmployeeQueryEngine

# Initialize the engine
engine = EmployeeQueryEngine("data/employees.xlsx")

# Get department statistics
dept_stats = engine.get_department_stats()

# Get seniority analysis
seniority = engine.get_seniority_analysis()

# Search by experience
senior_employees = engine.search_by_experience(min_years=5)

# Parse natural language
params = engine.parse_natural_language_query("Find senior developers in IT department")
```

## 🔒 Security Features

- **Input Validation** - Comprehensive input sanitization
- **CORS Configuration** - Configurable cross-origin requests
- **Rate Limiting** - Optional request rate limiting
- **Error Handling** - Secure error messages without data leakage
- **Local Processing** - No data leaves your infrastructure

## 📈 Monitoring & Health

### Health Check Response

```json
{
  "status": "healthy",
  "ollama_available": true,
  "faiss_index_loaded": true,
  "total_employees": 150
}
```

### System Statistics

```json
{
  "total_documents": 150,
  "embedding_model": "phi3",
  "llm_model": "phi3"
}
```

## 🚀 Deployment

### Local Development

The current setup is optimized for local development and proof of concept.

### Production Deployment (Future)

For Azure deployment, you would need to:

1. **Containerize the application** with Docker
2. **Set up Azure Container Instances** or **Azure App Service**
3. **Configure Azure Key Vault** for secrets management
4. **Set up Azure Monitor** for logging and monitoring
5. **Configure Teams Bot Framework** for Teams integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Ollama Connection Refused**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`

2. **FAISS Index Not Found**
   - Run the embedding script: `python -m rag_agent.embed_store`
   - Check the index path in configuration

3. **Excel File Not Found**
   - Ensure the Excel file exists in `data/employees.xlsx`
   - Check the file path in configuration

4. **Import Errors**
   - Activate the virtual environment
   - Install dependencies: `pip install -r requirements.txt`

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --log-level debug
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the test suite for examples
3. Check the API documentation at `/docs`
4. Open an issue on GitHub

---

**Built with ❤️ for secure, local AI-powered employee management**
