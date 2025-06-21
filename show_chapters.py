from chroma_store import collection
from rl_ranker import scores

print("\n All Saved Chapters:\n")

results = collection.get(include=["documents", "metadatas", "ids"])

for i in range(len(results["documents"])):
    doc = results["documents"][i][:300] + "..."  
    meta = results["metadatas"][i]
    doc_id = results["ids"][i]
    score = scores.get(doc_id, 0)

    print(f"[{i+1}] ID: {doc_id}")
    print(f" Source: {meta.get('source', 'Unknown')}")
    print(f" RL Score: {score}")
    print(f" Preview: {doc}")
    print("-" * 50)
