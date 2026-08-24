import os
import requests

def get_pr_diff(repo, pr_number, github_token):
    """
    Fetches the code changes (diff) from a specific Pull Request.

    repo: the repo name, like "yourusername/ai-pr-reviewer"
    pr_number: the PR number, like 1, 2, 3...
    github_token: a secret key that lets us talk to GitHub's API
    """

    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.diff"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch diff: {response.status_code} - {response.text}")


if __name__ == "__main__":
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    token = os.environ.get("GITHUB_TOKEN")

    diff = get_pr_diff(repo, pr_number, token)
    print(diff)
