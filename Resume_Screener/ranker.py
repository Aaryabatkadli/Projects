def rank_resumes(results):
    """
    Sort resumes by similarity score (higher is better)
    """
    return sorted(results, key=lambda x: x["score"], reverse=True)
