import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def analyze_resume(resume_text):
    if not resume_text.strip():
        return "No resume text available for analysis."

    prompt = (
        "Create a professional candidate summary from this resume.\n\n"
        "Include:\n"
        "- Candidate profile\n"
        "- Key skills\n"
        "- Experience summary\n\n"
        f"Resume:\n{resume_text[:1000]}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        if response.status_code != 200:
            return "AI analysis unavailable."

        data = response.json()
        return data.get("response", "No description generated.")

    except requests.exceptions.Timeout:
        return "AI analysis timed out. Try a smaller resume."

    except Exception as e:
        return f"AI analysis failed: {e}"
