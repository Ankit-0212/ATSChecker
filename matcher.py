# matcher.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc):
    docs = [resume_text, job_desc]
    tfidf = TfidfVectorizer().fit_transform(docs)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return score * 100  # Convert to percentage
