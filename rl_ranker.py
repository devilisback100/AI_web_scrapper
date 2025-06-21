scores = {}
ores = {}


def record_feedback(doc_id, reward):
    scores[doc_id] = scores.get(doc_id, 0) + reward


def re_rank(results):
    if not results or 'metadatas' not in results or not results['metadatas'] or not results['metadatas'][0]:
        return []
    for r in results['metadatas'][0]:
        r['rl_score'] = scores.get(r['id'], 0)
    return sorted(results['metadatas'][0], key=lambda x: x['rl_score'], reverse=True)
