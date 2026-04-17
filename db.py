import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/paraphrase-minilm-l6-v2')

FAQ_DATA = [
    "Blinkit delivers groceries in 10 minutes.",
    "The delivery fee is a flat 20 Rupees per order.",
    "We operate from 6 AM to midnight every day.",
    "You can track your order live through the 'My Orders' section.",
    "We accept UPI, credit/debit cards, and cash on delivery.",
    "Free delivery is available on orders above 500 Rupees.",
    "Fresh vegetables and fruits are sourced daily from local farms.",
    "Orders can only be canceled before the delivery partner picks them up.",
    "Refunds for canceled orders are processed within 5 to 7 business days.",
    "We currently serve major areas in Delhi, Mumbai, and Bangalore.",
    "Missing or damaged items can be reported via the in-app chat support.",
    "Our delivery partners follow strict hygiene and safety protocols.",
    "You can save multiple addresses like Home and Office in your profile.",
    "Membership subscribers get unlimited free delivery on all orders.",
    "We offer a wide range of organic and gluten-free products.",
    "All prices shown in the app are inclusive of GST and other taxes.",
    "You can rate your delivery experience and products after every order.",
    "Bulk orders for household essentials can be placed via the app.",
    "Milk and bread are available for early morning slots starting at 6 AM.",
    "Customer support is available 24/7 through the app's Help Center.",
    "Frozen items are transported in insulated bags to ensure they stay cold.",
    "You cannot reschedule an order once it has been placed.",
    "Promo codes can be applied on the checkout screen before payment.",
    "We do not provide phone support; please use our official in-app chat.",
    "Perishable items like milk must be checked at the time of delivery."
]

def seed_database():
    #  SQLite for Delta Logs
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delta_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            embedding TEXT,
            status TEXT DEFAULT 'unprocessed'
        )
    ''')
    conn.commit()
    conn.close()

    #  ChromaDB for Knowledge Base
    chroma_client = chromadb.PersistentClient(path="./vector_storage")
    # Delete if exists to avoid duplicates during testing
    try:
        chroma_client.delete_collection("knowledge_base")
    except:
        pass
        
    collection = chroma_client.create_collection(name="knowledge_base")
    
    print("Generating local embeddings using MiniLM-L6-v2...")
    embeddings = model.encode(FAQ_DATA).tolist()
    ids =[f"id_{i}" for i in range(len(FAQ_DATA))]

    collection.add(
        embeddings=embeddings,
        documents=FAQ_DATA,
        ids=ids
    )

    print(f"Success! Seeded {len(FAQ_DATA)} items into the Vector DB.")

if __name__ == "__main__":
    seed_database()