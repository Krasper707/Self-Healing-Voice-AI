import sqlite3
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-minilm-l6-v2')
queries =[
    "Do you guys have donut coupons?", 
    "Where is the discount code for donuts?",
    "Are there any donut promos?",
    "Fix my car tire" # Noise!
]

conn = sqlite3.connect('warehouse.db')
cursor = conn.cursor()
for q in queries:
    emb = model.encode(q).tolist()
    cursor.execute(
        "INSERT INTO delta_logs (query, embedding, status) VALUES (?, ?, ?)",
        (q, json.dumps(emb), "unprocessed")
    )
conn.commit()
conn.close()
print("✅ Simulated Traffic Injected: 'Donut Coupons' x3, 'Car Tire' x1")