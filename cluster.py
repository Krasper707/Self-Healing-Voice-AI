import sqlite3
import json
import os
import requests
import numpy as np
from sklearn.cluster import DBSCAN
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
model = SentenceTransformer('sentence-transformers/paraphrase-minilm-l6-v2')
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def verify_relevance(queries):
    """LLM Agent checks if the cluster is business-relevant."""
    prompt = f"Are these queries related to a grocery delivery app? Answer ONLY 'YES' or 'NO'. Queries: {queries}"
    res = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return "YES" in res.choices[0].message.content.upper()

def process_deltas():
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, query, embedding FROM delta_logs WHERE status = 'unprocessed'")
    rows = cursor.fetchall()
    
    if not rows:
        print("No unprocessed logs found.")
        return

    log_ids, queries, embeddings = [], [],[]
    for row in rows:
        log_ids.append(row[0]); queries.append(row[1]); embeddings.append(json.loads(row[2]))
        
    matrix = np.array(embeddings)
    print(f"🔍 Analyzing {len(queries)} missing queries...")

    # DBSCAN Clustering
    dbscan = DBSCAN(eps=0.3, metric="cosine", min_samples=2)
    labels = dbscan.fit_predict(matrix)

    clusters = {}
    for idx, label in enumerate(labels):
        if label == -1: continue # Drop Noise
        if label not in clusters: clusters[label] = {"ids": [], "queries": []}
        clusters[label]["ids"].append(log_ids[idx])
        clusters[label]["queries"].append(queries[idx])

    for label, data in clusters.items():
        if len(data["queries"]) > 1:
            print(f"\nFound High-Density Cluster: {data['queries'][:2]}...")
            
            # VERIFICATION AGENT
            print("🧐 Verification Agent checking business relevance...")
            if not verify_relevance(data["queries"]):
                print("Agent Rejected: Out of Domain.")
                continue
                
            # AUTO-DRAFTING
            prompt = f"""
            You are a Customer Experience Manager at Blinkit. 
            Multiple users have repeatedly asked the following questions: {data['queries']}
            
            Identify the core product, feature, or promotion they are asking for. 
            Draft EXACTLY ONE professional sentence to be added to our official FAQ Knowledge Base. 
            The sentence should politely acknowledge the topic and inform the user that Blinkit is actively working on bringing this to the platform soon.
            
            CRITICAL: Do not include any introductions, explanations, or quotes. Output ONLY the 1-sentence policy.
            """
            draft = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant", 
                messages=[{"role": "user", "content": prompt}],temperature=0.2
            ).choices[0].message.content.strip()
            
            # HUMAN IN THE LOOP
            print(f"PROPOSED KB UPDATE: '{draft}'")
            if input("Approve update? (y/n): ").lower() == 'y':
                emb = model.encode(draft).tolist()
                requests.post("http://localhost:8000/add-policy", json={"text": draft, "embedding": emb})
                
                # Mark processed
                placeholders = ','.join(['?'] * len(data['ids']))
                cursor.execute(f"UPDATE delta_logs SET status = 'processed' WHERE id IN ({placeholders})", data['ids'])
                conn.commit()
                print("Deployed to Production.")
    conn.close()

if __name__ == "__main__":
    process_deltas()