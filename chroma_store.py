import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
collection = client.get_or_create_collection(name="chapters")
embedding_func = embedding_functions.DefaultEmbeddingFunction()


def save_to_chroma(text, meta):
    collection.add(documents=[text], metadatas=[meta], ids=[meta['id']])


def search_chroma(query):
    return collection.query(query_texts=[query], n_results=5, include=['documents', 'metadatas'])


def list_all_documents():
    results = collection.get()
    docs = results.get('documents', [])
    metadatas = results.get('metadatas', [])

    if not docs:
        print(" No files found in ChromaDB.")
        return []

    print("\n Stored Chapters:\n")
    for i, meta in enumerate(metadatas):
        print(f"{i+1}. ID: {meta.get('id')} | Source: {meta.get('source')}")
        print(f"   Preview: {docs[i][:150].strip()}...\n")

    return list(zip(docs, metadatas))  


def get_document_by_index(index: int):
    results = collection.get()
    documents = results.get('documents', [])
    metadatas = results.get('metadatas', [])

    if 0 <= index < len(documents):
        return documents[index], metadatas[index]
    return None, None
