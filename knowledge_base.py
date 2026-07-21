"""Knowledge base + retrieval for RAG-style explanation.
WHY RAG: instead of letting an LLM guess why something was flagged, we
retrieve a matching known signature and ground the explanation in it.
No external vector DB or API key needed -- TF-IDF is enough at this scale.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SIGNATURES = [
    {"id": "SIG-1", "text": "Constant position drift: GPS reports steady "
     "movement while inertial sensors show no acceleration, typical of "
     "simple GPS spoofing."},
    {"id": "SIG-2", "text": "Sudden altitude jump attack: GPS altitude "
     "changes abruptly without matching barometric or IMU data, common in "
     "signal replay attacks."},
    {"id": "SIG-3", "text": "Speed mismatch anomaly: reported GPS speed "
     "diverges sharply from IMU-derived speed, suggesting spoofed or "
     "jammed satellite signal."},
    {"id": "SIG-4", "text": "Normal flight pattern: GPS and IMU readings "
     "are consistent, no attack indicators present."},
]

_vectorizer = TfidfVectorizer().fit([s["text"] for s in SIGNATURES])
_matrix = _vectorizer.transform([s["text"] for s in SIGNATURES])


def retrieve(query: str, top_k: int = 1):
    q_vec = _vectorizer.transform([query])
    sims = cosine_similarity(q_vec, _matrix)[0]
    idx = sims.argsort()[::-1][:top_k]
    return [SIGNATURES[i] for i in idx]
