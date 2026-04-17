
# Blinkit Voice AI & Self-Healing RAG Pipeline

An enterprise-grade, ultra-low latency Voice AI Assistant designed for Quick Commerce (Blinkit). This architecture not only handles real-time Voice-to-Voice customer service but actively detects its own knowledge gaps (Deltas) and autonomously drafts new policies to self-heal the Knowledge Base.

## Core Architectural Innovations

[![](https://mermaid.ink/img/pako:eNqFVW1z4jYQ_isa3xeYsSlgyBlfX4aE0DA1yV0MdFon0xH2GlRkybXkXCjkv3ctw8W9y7T-oJFW-zza1T4rH6xYJmD51qag-ZYsJg-C4BdzqtQEUlIA5QuWAUkZ5_47cNN-mthKF3IH_rtB3xumg9PS-cwSvfX7-fOHr0hkmnImzhxpL_Vg9IXD9Txw4__lSNZneJq60P0CT9dxt5-8Ba8JVLmuU7vHTByTykqyGEggZR6F5doZdruZIgHVIOL9Y42qvmWrtVRQ1O7tNnGcH49zFh9JuFhEv26ZynET5w0IrozbAp71kVxna0iiQMaUkzkTLJjXpoSJTQNkbBWMrMLofjwnK4i1RGqgRbxtOL7OVqHxn1O9PVxJVd1tyDLyPel23OFPL29BKl8Ekd-uQ9KaANfUZESm02hKlXamlHEypZyvabxrHDqdmozGai9icol7m0KWIiELqnZHYsyB3ESt8FPANPgkqaj_4HKj2o--7yfrr6nIYhFG18kGqsnjf4V6e0daM-FMZEaZqKP9uZB_RdVAAk4z6rgNAmM-HfBqxYUxhjnQHRSt1mlC7kqdl7rdrl1BJA3BkaWNpbRNZexVaFcR2dOpXR1hI6N9Jjm3x7dyGwd3uSIfWQ5G-lEIPHVu0B2LT34R8jMHvING-OerrKsCOt5GZiRLkRcyBqVQJZ9KKBioZn2MT4WZXIZX49sojNmOaSdA9YiTreFeG0xJMZkyJ-s9mQmUPup1yriGIpoUMie3kikg35GZkhw7g1zxUuGmerNgNbCWMMaXRmZkMdVMCjLeIHsDZzZNBPfA4YmKGH5YFCUcyaSgqY4C7JNxqaVjluSj5OxffdlIxjhUx97MFsHhpsyocJhwqtZuNEG1WelpnONFPoEBzMSf2GVRa5knJr1tgSqbXH6j2dqvVhDWJwoYEoRQPGG-c8hksceHhUuaNF-BqlWcDiZYs6sjNuybMjPFs-ua2PUt2uZ6bJOaXUVuG7rTE_rBsvGlZonlp5QrsK0MCuwOXFuHivjB0lvI4MHycZpASkuuH6wH8YK4nIrfpcwsX-Nl2xZWf7M9L0oT6IRRFO-rB0YLxRW2u7b8oWcYLP9gPVt-zxt0vP7FqD_suYPusHsxsK295Tt996Iz8ryh-94dDS_63YH3Ylt_m1N7nb47GvSGXs99P_Bc10VCSBi-dPP6D2R-RC__AEA1AV4?type=png)](https://mermaid.live/edit#pako:eNqFVW1z4jYQ_isa3xeYsSlgyBlfX4aE0DA1yV0MdFon0xH2GlRkybXkXCjkv3ctw8W9y7T-oJFW-zza1T4rH6xYJmD51qag-ZYsJg-C4BdzqtQEUlIA5QuWAUkZ5_47cNN-mthKF3IH_rtB3xumg9PS-cwSvfX7-fOHr0hkmnImzhxpL_Vg9IXD9Txw4__lSNZneJq60P0CT9dxt5-8Ba8JVLmuU7vHTByTykqyGEggZR6F5doZdruZIgHVIOL9Y42qvmWrtVRQ1O7tNnGcH49zFh9JuFhEv26ZynET5w0IrozbAp71kVxna0iiQMaUkzkTLJjXpoSJTQNkbBWMrMLofjwnK4i1RGqgRbxtOL7OVqHxn1O9PVxJVd1tyDLyPel23OFPL29BKl8Ekd-uQ9KaANfUZESm02hKlXamlHEypZyvabxrHDqdmozGai9icol7m0KWIiELqnZHYsyB3ESt8FPANPgkqaj_4HKj2o--7yfrr6nIYhFG18kGqsnjf4V6e0daM-FMZEaZqKP9uZB_RdVAAk4z6rgNAmM-HfBqxYUxhjnQHRSt1mlC7kqdl7rdrl1BJA3BkaWNpbRNZexVaFcR2dOpXR1hI6N9Jjm3x7dyGwd3uSIfWQ5G-lEIPHVu0B2LT34R8jMHvING-OerrKsCOt5GZiRLkRcyBqVQJZ9KKBioZn2MT4WZXIZX49sojNmOaSdA9YiTreFeG0xJMZkyJ-s9mQmUPup1yriGIpoUMie3kikg35GZkhw7g1zxUuGmerNgNbCWMMaXRmZkMdVMCjLeIHsDZzZNBPfA4YmKGH5YFCUcyaSgqY4C7JNxqaVjluSj5OxffdlIxjhUx97MFsHhpsyocJhwqtZuNEG1WelpnONFPoEBzMSf2GVRa5knJr1tgSqbXH6j2dqvVhDWJwoYEoRQPGG-c8hksceHhUuaNF-BqlWcDiZYs6sjNuybMjPFs-ua2PUt2uZ6bJOaXUVuG7rTE_rBsvGlZonlp5QrsK0MCuwOXFuHivjB0lvI4MHycZpASkuuH6wH8YK4nIrfpcwsX-Nl2xZWf7M9L0oT6IRRFO-rB0YLxRW2u7b8oWcYLP9gPVt-zxt0vP7FqD_suYPusHsxsK295Tt996Iz8ryh-94dDS_63YH3Ylt_m1N7nb47GvSGXs99P_Bc10VCSBi-dPP6D2R-RC__AEA1AV4)
### Semantic Routing (The "Fast-Fail" Latency Hack)
Voice AI requires sub-500ms latency. Sending every query to an LLM is too slow and expensive. 
This system uses **Local Embeddings (MiniLM)** and **Cosine Similarity Math** to route queries:
- **In-Domain (Similarity > 0.35):** Routed to Groq (Llama-3) for a rapid conversational response.
- **Out-of-Domain / Delta (Similarity < 0.35):** Bypasses the LLM entirely, returning a 30ms fallback response ("I'll let my team know!"). 

### Asynchronous Delta Logging
When a missing query is detected, it is logged to an SQLite database using FastAPI `BackgroundTasks`. This ensures Disk I/O does not block the real-time Voice TTS stream.

### ALOps (Active Learning Operations)
A simulated nightly cron job analyzes the Delta logs using **DBSCAN Clustering**. It filters out random noise and identifies high-density clusters (e.g., multiple users asking for "donut coupons").

### Multi-Agent Verification & Human-in-the-Loop (HITL)
Once a cluster is found, the system utilizes a **Verification Agent** (LLM) using Chain-of-Thought to ensure the topic is business-relevant. If verified, it auto-drafts a Knowledge Base policy and waits for a Human Manager to click "Approve" before injecting it into the live Vector DB.

---

## Tech Stack

- **Backend:** FastAPI, Python `asyncio`
- **Voice I/O:** OpenAI Whisper (STT), Edge-TTS, Web Speech API
- **LLM Engine:** Groq (Llama-3.1-8b-instant) for >800 T/s inference speed
- **Vector DB & Embeddings:** ChromaDB, `sentence-transformers` (Local)
- **Clustering:** Scikit-Learn (DBSCAN), Numpy, Scipy

---

## Installation & Setup

1. **Clone and Install Dependencies:**
   ```bash
   uv venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   uv pip install fastapi uvicorn groq scikit-learn numpy scipy SpeechRecognition pyaudio pygame requests python-dotenv sentence-transformers chromadb edge-tts
   ```

2. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

3. **Initialize the Database:**
   ```bash
   python seed_db.py
   ```

---

## How to Run the Demo

This project is designed to be demonstrated in a 4-step narrative flow.

### Step 1: Start the Backend Server
```bash
uvicorn backend:app --port 8000
```
*(Leave this running in Terminal 1. Note the RAM injection logs).*

### Step 2: Test the Fast-Fail Baseline
Open your browser to `http://localhost:8000` (or run `python voice_client.py`).
- **Ask:** *"How much is the delivery fee?"* -> Bot successfully answers via RAG.
- **Ask:** *"Do you have donut coupons?"* -> Bot instantly fast-fails, bypassing the LLM to save latency, and asynchronously logs the Delta.

### Step 3: Simulate Traffic & Run ALOps
In Terminal 2, simulate a spike in missing customer queries:
```bash
python dummy_traffic.py
```
Then, run the clustering and auto-drafting pipeline:
```bash
python offline_clustering.py
```
- Watch the Terminal filter out noise, verify business relevance, and auto-draft a Donut policy.
- Press `y` to approve the update (HITL). Watch Terminal 1 dynamically reload its memory without dropping the server.

### Step 4: The Self-Healed Resolution
Return to the Voice Client.
- **Ask:** *"Do you have donut coupons?"*
- The bot will now instantly and correctly answer the question based on the newly injected Knowledge Base article.
