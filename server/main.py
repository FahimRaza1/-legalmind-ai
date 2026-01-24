from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import chromadb
import os
import shutil
import fitz  # PyMuPDF

# Chunking configuration
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 50  # Overlap to maintain context

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

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text from the saved PDF
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    
    # NEW: Simple Semantic Chunking
    chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)]
    
    # Store in ChromaDB
    client = chromadb.HttpClient(host='chroma', port=8000)
    collection = client.get_or_create_collection(name="legal_docs")
    
    # Add chunks to the vector database
    collection.add(
        documents=chunks,
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file.filename} for _ in range(len(chunks))]
    )
    
    return {
        "message": "Ingested into Vector DB",
        "chunks_created": len(chunks),
        "total_chars": len(text)
    }
