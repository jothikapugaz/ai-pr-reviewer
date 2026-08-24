import subprocess
import os

def run_pylint(filepath):
    """Runs pylint on a file and returns its findings as text."""
    result = subprocess.run(
        ["pylint", filepath, "--disable=all", "--enable=E,W", "--score=n"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def run_bandit(filepath):
    """Runs bandit (security scanner) on a file and returns its findings."""
    result = subprocess.run(
        ["bandit", "-f", "txt", filepath],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def analyze_file(filepath):
    """Runs both tools on one file and combines the results."""
    pylint_output = run_pylint(filepath)
    bandit_output = run_bandit(filepath)

    return f"""--- Pylint findings for {filepath} ---
{pylint_output if pylint_output else "No issues found."}

--- Bandit security findings for {filepath} ---
{bandit_output if bandit_output else "No issues found."}
"""


if __name__ == "__main__":
    # Reads a list of changed .py files (one per line) from changed_files.txt
    with open("changed_files.txt", "r") as f:
        files = [line.strip() for line in f if line.strip().endswith(".py")]

    all_results = ""
    for file in files:
        if os.path.exists(file):
            all_results += analyze_file(file) + "\n"

    with open("static_analysis.txt", "w") as f:
        f.write(all_results if all_results else "No Python files changed.")

    print(all_results)
