import sqlite3
import json
import os
import uuid
import numpy as np
from scipy.spatial.distance import cosine
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from contextlib import asynccontextmanager

import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

load_dotenv()

import edge_tts

async def generate_voice_file(text: str, filename: str):
    communicate = edge_tts.Communicate(text, "en-IN-NeerjaNeural")
    await communicate.save(filename)

kb_documents = []
kb_embeddings =[]

model = SentenceTransformer('sentence-transformers/paraphrase-minilm-l6-v2')
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./vector_storage")
collection = chroma_client.get_collection(name="knowledge_base")

def load_data():
    """Fetches rows from ChromaDB into RAM for ultra-fast vector math."""
    global kb_documents, kb_embeddings
    data = collection.get(include=["embeddings", "documents"])
    
    if data and data["documents"]:
        kb_documents = data["documents"]
        kb_embeddings = np.array(data["embeddings"])
        print(f"\nMEMORY REFRESHED: Loaded {len(kb_documents)} items.")
        print(f"Newest Policy: '{kb_documents[-1]}'\n")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up... Loading knowledge base into RAM.")
    load_data()
    yield
    print("Shutting down.")

app = FastAPI(lifespan=lifespan)

class ChatRequest(BaseModel):
    query: str

class PolicyRequest(BaseModel):
    text: str
    embedding: list[float]

from fastapi.staticfiles import StaticFiles
if not os.path.exists("static"): os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

def log_delta_to_sqlite(query: str, embedding_vector: list):
    """Saves unresolved queries in the background without blocking the Voice API."""
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO delta_logs (query, embedding, status) VALUES (?, ?, ?)",
        (query, json.dumps(embedding_vector), "unprocessed")
    )
    conn.commit()
    conn.close()
    print(f"Asynchronously Logged Delta: '{query}'")

# @app.post("/voice-chat")
# async def voice_chat(request: ChatRequest, background_tasks: BackgroundTasks):
#     user_query = request.query
#     query_vector = model.encode(user_query).tolist()
    
#     max_similarity = -1.0
#     best_chunk = ""
    
#     # Fast Local Vector Search (O(N) in RAM)
#     for i, kb_emb in enumerate(kb_embeddings):
#         sim = 1 - cosine(query_vector, kb_emb)
#         if sim > max_similarity:
#             max_similarity = sim
#             best_chunk = kb_documents[i]
            
#     print(f"🗣️ User: '{user_query}' | 🧮 Sim: {max_similarity:.4f} | 📄 Match: '{best_chunk[:40]}...'")

#     # SEMANTIC ROUTING (Threshold set to 0.35 for MiniLM)
#     if max_similarity < 0.35:
#         # Fast-Fail: Bypass LLM to save tokens/latency
#         background_tasks.add_task(log_delta_to_sqlite, user_query, query_vector)
#         return {"response": "I don't have information on that yet, but I'll let my team know."}
        
#     else:
#         # In-Domain: Generate answer using Groq Llama-3
#         prompt = f"Answer concisely for voice. Context: {best_chunk}. Query: {user_query}"
#         response = groq_client.chat.completions.create(
#             model="llama-3.1-8b-instant", 
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3
#         )
#         return {"response": response.choices[0].message.content}

@app.post("/voice-chat")
async def voice_chat(request: ChatRequest, background_tasks: BackgroundTasks):
    user_query = request.query
    query_vector = model.encode(user_query).tolist()
    
    max_similarity = -1.0
    best_chunk = ""
    
    for i, kb_emb in enumerate(kb_embeddings):
        sim = 1 - cosine(query_vector, kb_emb)
        if sim > max_similarity:
            max_similarity = sim
            best_chunk = kb_documents[i]
            
    print(f"User: '{user_query}' | Sim: {max_similarity:.4f}")

    # Determine the TEXT response first
    if max_similarity < 0.35:
        bot_response_text = "I don't have information on that yet, but I'll let my team know!"
        # Log the delta in the background
        background_tasks.add_task(log_delta_to_sqlite, user_query, query_vector)
    else:
        prompt = f"Answer concisely for voice. Context: {best_chunk}. Query: {user_query}"
        # Use a variable name 
        llm_response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        bot_response_text = llm_response.choices[0].message.content

    # Generate the AUDIO for the response 
    audio_filename = f"static/resp_{uuid.uuid4().hex[:8]}.mp3"
    await generate_voice_file(bot_response_text, audio_filename)
    
    # 3. Return both to the frontend
    return {
        "response": bot_response_text,
        "audio_url": f"/{audio_filename}" 
    }
@app.post("/add-policy")
async def add_policy(request: PolicyRequest):
    """Endpoint for ALOps script to inject new knowledge."""
    new_id = f"auto_{uuid.uuid4().hex[:8]}"
    collection.add(
        embeddings=[request.embedding],
        documents=[request.text],
        ids=[new_id]
    )
    load_data() # Live reload RAM
    return {"status": "Success"}

@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return FileResponse("index.html")
