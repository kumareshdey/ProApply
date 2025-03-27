import hashlib
from creds import GROQ_API_KEY
import os
import openai
from sentence_transformers import SentenceTransformer
import chromadb


client = openai.OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
chroma_client = chromadb.PersistentClient(path="db")
embedding_model = SentenceTransformer("BAAI/bge-large-en-v1.5")


def genai_model(query):
    # completion = client.chat.completions.create(
    #     model="llama-3.3-70b-versatile",
    #     messages=[],
    #     temperature=1,
    #     max_completion_tokens=1024,
    #     top_p=1,
    #     stream=True,
    #     stop=None,
    # )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": query}],
        temperature=0.7,
    )
    return [choice.message.content for choice in response.choices]


def generate_embeddings(text):
    embedding = embedding_model.encode(text)
    return embedding


def store_embedding(text, embedding, user_id=1):
    collection = chroma_client.get_or_create_collection(f"user_data_{user_id}")
    id = hashlib.sha256(text.encode()).hexdigest()
    existing_data = collection.get(ids=[id])
    if existing_data and existing_data["ids"]:
        print("⚠️ Text already exists in ChromaDB, skipping embedding.")
        return id
    embedding = embedding_model.encode(text)
    collection.add(documents=[text], embeddings=[embedding.tolist()], ids=[id])
    print("✅ New text stored in ChromaDB.")
    return id


def query_similar_texts(query, user_id=1, threshold=1, n_results=10):
    print("Querying similar texts for : ", query)
    collection = chroma_client.get_or_create_collection(f"user_data_{user_id}")
    query_embedding = generate_embeddings(query)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        include=["documents", "distances"],
    )
    retrieved_data = []
    for doc, score in zip(results["documents"][0], results["distances"][0]):
        if score <= threshold:
            retrieved_data.append(doc)
    print(f"Queried {len(retrieved_data)} documents")
    return retrieved_data
