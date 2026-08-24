import os
import requests

def review_code(diff, groq_api_key):
    """
    Sends the code diff to the Groq AI API and asks it to act as a
    senior code reviewer. Returns the AI's written review as text.
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""You are a senior software engineer doing a code review.
Review the following code diff. Point out:
- Bugs or logic errors
- Security issues
- Style/readability problems
- Missing edge case handling

Be specific and reference the actual lines when possible.
Keep your review concise and use markdown formatting with headers and bullet points.

Here is the diff:

{diff}
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

    review = review_code(diff, groq_api_key)
    print(review)
