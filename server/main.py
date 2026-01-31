from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import chromadb
import os
import shutil
import fitz  # PyMuPDF
import requests

# Chunking configuration
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 50  # Overlap to maintain context

# Replace 'hf_your_token_here' with the actual token you just copied
# 1. Use the specific "feature-extraction" pipeline URL
API_URL = "https://router.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

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


def get_embeddings(texts):
    # Use the feature-extraction pipeline
    API_URL = "https://router.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}
    
    # The "wait_for_model" option tells Hugging Face to hold the request until the model is loaded
    payload = {
        "inputs": texts,
        "options": {"wait_for_model": True} 
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    
    # ADD THIS PRINT LINE:
    print(f"DEBUG HF API: Status {response.status_code} | Body: {response.text}")
    
    if response.status_code == 200:
        return response.json()
    return None

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
    
    # Simple Semantic Chunking
    chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP)]
    
    # 1. Turn chunks into Vectors (Embeddings) via Hugging Face API
    embeddings = get_embeddings(chunks)

    # 2. Store in ChromaDB
    client = chromadb.HttpClient(host='chroma', port=8000)
    collection = client.get_or_create_collection(name="legal_docs")
    
    collection.add(
        embeddings=embeddings,  # Now we are adding the actual "brain" data
        documents=chunks,
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file.filename} for _ in range(len(chunks))]
    )
    
    return {"status": "Vector Database Updated", "chunks": len(chunks), "total_chars": len(text), "filename": file.filename}

# Use a distance threshold (0.0 is perfect match, 2.0 is opposite)
# 0.4 to 0.6 is usually the "sweet spot" for relevance
THRESHOLD = 0.5

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_document(request: QueryRequest):
    raw_output = get_embeddings([request.question])
    
    # If the AI is busy, let's try a simple text search in ChromaDB instead
    client = chromadb.HttpClient(host='chroma', port=8000)
    collection = client.get_or_create_collection(name="legal_docs")

    if not raw_output:
        # FALLBACK: Search by keywords if the AI vectorizer is down
        results = collection.query(
            query_texts=[request.question], # ChromaDB can do basic text matching too!
            n_results=1
        )
        if results['documents'][0]:
            return {"answer": f"(Keyword Match): {results['documents'][0][0]}"}
        return {"answer": "AI is still loading. Please refresh and try in 30 seconds."}

    # Hugging Face returns a 3D list [[[...]]], we need a 1D list [...]
    # This 'flattens' the response so ChromaDB can read it
    try:
        if isinstance(raw_output, list):
            # Navigate through the nesting until we find the list of floats
            vector = raw_output[0]
            if isinstance(vector, list) and isinstance(vector[0], list):
                vector = vector[0]
        else:
            return {"answer": "Unexpected data format from AI."}
    except Exception as e:
        print(f"Flattening error: {e}")
        return {"answer": "Error processing AI data."}
    
    # When searching, ask for the "distances" too
    results = collection.query(
        query_embeddings=[vector], 
        n_results=1,
        include=["documents", "distances"] # Add this!
    )
    
    # Check if the match is "close" enough
    distance = results['distances'][0][0]
    
    if distance > THRESHOLD:
        return {"answer": "I'm sorry, that information is not in the uploaded document."}

    # If it's a good match, return the text
    answer = results['documents'][0][0]
    return {"answer": f"According to the document: {answer}"}
    
    return {"answer": "I couldn't find any information about that in the uploaded file."}