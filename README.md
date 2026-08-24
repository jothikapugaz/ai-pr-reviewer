🤖 AI PR Reviewer

Automated, AI-powered code reviews for GitHub Pull Requests — grounded in real static analysis, not raw LLM guesses.

"GitHub Actions" (https://img.shields.io/badge/CI-GitHub%20Actions-blue)
"Python" (https://img.shields.io/badge/Python-3.11-yellow)
"License" (https://img.shields.io/badge/License-MIT-green)

---

🚀 Overview

AI PR Reviewer is an automated GitHub Pull Request reviewer that combines static code analysis with LLM-powered reasoning to provide fast, useful, and trustworthy code reviews.

Instead of asking an LLM to review code blindly, the system first runs Pylint and Bandit to identify verified issues. These findings are then provided to the LLM, which explains them in plain language and adds clearly labeled observations.

This approach helps reduce one of the biggest problems with AI code review: confidently incorrect findings.

The core idea

«Static analysis provides the facts.
AI provides the reasoning.
Humans make the final decision.»

---

✨ Why This Exists

Traditional code reviews can be time-consuming, while purely LLM-based reviewers can produce hallucinated or misleading feedback.

AI PR Reviewer combines both approaches:

- 🔍 Pylint — identifies verified Python code-quality issues
- 🔐 Bandit — detects common security vulnerabilities
- 🧠 Groq LLM — explains findings and provides additional insights
- ⚡ GitHub Actions — automatically runs the review whenever a PR changes
- 💬 GitHub API — posts the final review directly to the Pull Request

The result is a fast first-pass reviewer with a clear distinction between verified findings and AI-generated observations.

---

🎥 See It In Action

Check out "PR #1" (../../pull/1) for a complete live example.

It demonstrates the review workflow and includes a before/after comparison showing how grounding the LLM in static-analysis results helps eliminate false claims.

---

🏗️ Architecture

                    ┌─────────────────────┐
                    │   Pull Request      │
                    │   Opened / Updated  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   GitHub Actions    │
                    │      Trigger        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Fetch PR Diff     │
                    │    GitHub REST API  │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │       Static Analysis            │
              │                                  │
              │   Pylint          Bandit         │
              │      │              │             │
              │      └──────┬───────┘             │
              │             ▼                     │
              │      Confirmed Findings           │
              └─────────────┬────────────────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Groq LLM        │
                 │                      │
                 │  PR Diff + Verified  │
                 │      Findings        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Structured Review  │
                 │   Posted to GitHub   │
                 └──────────────────────┘

---

🔄 How It Works

1. A Pull Request is opened or updated.
2. GitHub Actions automatically triggers the workflow.
3. The PR diff is retrieved through the GitHub REST API.
4. Changed Python files are analyzed using Pylint and Bandit.
5. Confirmed static-analysis findings are collected.
6. The PR diff and verified findings are sent to the Groq LLM.
7. The LLM explains the confirmed issues and provides additional observations.
8. The final structured review is posted as a comment on the Pull Request.

---

📁 Project Structure

.github/
└── workflows/
    └── review.yml          # GitHub Actions workflow

src/
├── fetch_diff.py           # Fetches PR changes through GitHub API
├── static_analysis.py      # Runs Pylint and Bandit
├── llm_review.py           # Sends findings + diff to Groq
└── post_comment.py         # Posts the review to the PR

---

🧠 Engineering Highlights

1. Hallucination Mitigation

The LLM isn't treated as the source of truth.

Static-analysis results are explicitly provided as confirmed findings, while additional AI observations are clearly separated.

The prompt also instructs the model to avoid presenting uncertain conclusions as facts.

This creates a simple but important distinction:

CONFIRMED
├── Pylint findings
└── Bandit findings

AI OBSERVATIONS
├── Possible improvements
├── Maintainability suggestions
└── Other reasoning-based feedback

---

2. Least-Privilege GitHub Permissions

The GitHub Actions workflow follows the principle of least privilege.

Required permissions are limited to:

permissions:
  contents: read
  pull-requests: write

The workflow can read repository contents and publish Pull Request feedback without granting unnecessary repository permissions.

---

3. No Hardcoded Secrets

API credentials are never stored in source code.

The Groq API key is securely provided through GitHub Actions Secrets:

GROQ_API_KEY

This keeps sensitive credentials outside the repository.

---

4. Serverless Architecture

The project requires no dedicated backend server or database.

Everything runs on GitHub-hosted runners:

GitHub PR
    ↓
GitHub Actions
    ↓
Python scripts
    ↓
Pylint / Bandit
    ↓
Groq API
    ↓
GitHub PR Comment

This keeps the infrastructure simple, inexpensive, and easy to maintain.

---

🛠️ Tech Stack

Layer| Technology
CI/CD| GitHub Actions
Language| Python 3.11
LLM Inference| Groq API
LLM Model| "openai/gpt-oss-120b"
Static Analysis| Pylint
Security Analysis| Bandit
Integration| GitHub REST API
Hosting| GitHub Actions

---

⚙️ Setup

1. Clone or copy the project

Copy the following into your repository:

.github/workflows/review.yml
src/

2. Create a Groq API Key

Create an API key through the "Groq Console" (https://console.groq.com).

3. Add the API Key to GitHub

Navigate to:

Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret

Create:

Name: GROQ_API_KEY
Value: <your-api-key>

4. Open a Pull Request

Once the workflow is configured, open or update a Pull Request.

GitHub Actions will automatically run the reviewer and post the generated review as a PR comment.

---

📋 Example Review Flow

Pull Request
     │
     ├── Code Diff
     │
     ├── Pylint
     │     └── Confirmed findings
     │
     └── Bandit
           └── Confirmed security findings
                 │
                 ▼
              Groq LLM
                 │
                 ▼
        ┌─────────────────────┐
        │ AI PR Review        │
        │                     │
        │ ✓ Confirmed Issues  │
        │ ✓ Security Findings│
        │ 💡 AI Observations │
        └─────────────────────┘

---

⚠️ Limitations

AI PR Reviewer is designed as a first-pass assistant, not a replacement for human code review.

The additional observations section is generated by the LLM and may occasionally contain incorrect or incomplete suggestions.

For this reason:

- Static-analysis findings are treated as verified evidence.
- AI-generated observations are clearly labeled.
- Human developers remain responsible for the final review and decision.

---

🗺️ Roadmap

- [ ] Add JavaScript/TypeScript support using ESLint
- [ ] Add inline comments on specific changed lines
- [ ] Add configurable severity thresholds

---

🔒 Security Philosophy

The project follows three core principles:

Verify before explaining.

Use deterministic static-analysis tools to establish facts before asking the LLM to reason about the code.

Minimize permissions.

Give GitHub Actions only the permissions required to perform its job.

Keep humans in the loop.

AI-generated feedback should assist developers, not replace engineering judgment.

---

📄 License

This project is licensed under the MIT License.

---

<div align="center">Built to explore how AI-assisted code review can be made faster, safer, and more reliable.

⭐ If you find the project interesting, consider giving it a star!

</div>
