"""
Enterprise ranking engine (skills + experience only)
"""

def rank_candidates(jd_skills, jd_exp, resumes):
    ranked = []

    for res in resumes:
        score = 0

        # ---- Skill match (60%) ----
        skills = res["metadata"].get("skills", [])
        if jd_skills:
            matched = len(set(jd_skills) & set(skills))
            skill_score = (matched / len(jd_skills)) * 60
        else:
            skill_score = 0

        # ---- Experience match (40%) ----
        exp = res["metadata"].get("experience", 0)
        if jd_exp:
            if exp >= jd_exp:
                exp_score = 40
            else:
                exp_score = (exp / jd_exp) * 40
        else:
            exp_score = 0

        res["score"] = round(skill_score + exp_score, 2)
        ranked.append(res)

    return sorted(ranked, key=lambda x: x["score"], reverse=True)
