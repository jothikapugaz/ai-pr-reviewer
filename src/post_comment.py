import os
import requests

def post_pr_comment(repo, pr_number, comment_body, github_token):
    """
    Posts a comment on a specific Pull Request.

    repo: "yourusername/ai-pr-reviewer"
    pr_number: the PR number
    comment_body: the text of the comment (our AI review)
    github_token: secret key to authenticate with GitHub
    """

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "body": comment_body
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        raise Exception(f"Failed to post comment: {response.status_code} - {response.text}")


if __name__ == "__main__":
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")

    with open("review.txt", "r") as f:
        review = f.read()

    header = "## 🤖 AI Code Review\n\n"
    footer = "\n\n---\n*This review was generated automatically by an AI reviewer bot.*"
    full_comment = header + review + footer

    post_pr_comment(repo, pr_number, full_comment, token)
