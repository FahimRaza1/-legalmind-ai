from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import chromadb
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    # Test Postgres Connection
    db_status = "Down"
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        db_status = "Connected"
        conn.close()
    except Exception as e:
        db_status = f"Error: {str(e)}"

    # Test ChromaDB Connection
    chroma_status = "Down"
    try:
        # Note: 'chroma' is the service name from your docker-compose
        client = chromadb.HttpClient(host='chroma', port=8000)
        client.heartbeat()
        chroma_status = "Connected"
    except Exception as e:
        chroma_status = f"Error: {str(e)}"

    return {
        "api": "Running",
        "postgres": db_status,
        "chroma": chroma_status
    }
