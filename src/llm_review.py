import os
import requests

def review_code(diff, static_findings, groq_api_key):
    """
    Sends the code diff AND real static analysis results to the Groq AI API
    and asks it to act as a senior code reviewer. Returns the AI's written review.
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a senior software engineer doing a code review.

Below are two things:
1. The code diff (the actual changes)
2. CONFIRMED findings from real static analysis tools (pylint + bandit) — these are FACTS, not guesses.

Your job:
- Explain and expand on the confirmed findings in plain, helpful language
- Only add NEW observations beyond the confirmed findings if you are highly confident they are real issues
- If you are not sure something is an issue, say "possible issue" instead of stating it as fact
- Do NOT invent problems about tools, configs, or permissions unless you can see clear evidence in the diff
- Keep it concise, use markdown with headers and bullet points

--- CODE DIFF ---
{diff}

--- CONFIRMED STATIC ANALYSIS FINDINGS ---
{static_findings}
"""

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API error: {response.status_code} - {response.text}")


if __name__ == "__main__":
    groq_api_key = os.environ.get("GROQ_API_KEY")

    with open("diff.txt", "r") as f:
        diff = f.read()

    with open("static_analysis.txt", "r") as f:
        static_findings = f.read()

    review = review_code(diff, static_findings, groq_api_key)
    print(review)
