import requests
import time
import sys
import os

# Wait for services to be up (simplified)
time.sleep(5)

JIRA_URL = "http://mock-jira:5000/rest/api/3/issue/PROJ-123"
OLLAMA_URL = "http://ollama:11434/api/chat"

# MODEL = os.environ['OLLAMA_MODEL']

def check_pr_against_ticket(jira_summary, jira_criteria, pr_summary, code_diff):
    prompt = f"""
JIRA Ticket:
Summary: {jira_summary}
Acceptance Criteria: {jira_criteria}

Pull Request:
Summary: {pr_summary}
Code Diff:
{code_diff[:3000]}

Does the PR meet the Jira requirements?
"""

    model = os.environ['OLLAMA_MODEL']
    sys.stdout.write("Using model: " + model + "\n")

    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })

    sys.stdout.write("Chat status: " + str(response.status_code) + "\n")

    result = response.json()
    return result["message"]["content"]

def main():
    # Fake PR summary + diff
    pr_summary = "Added login form with username and password input fields."
    code_diff = "diff --git a/LoginPage.js b/LoginPage.js\n+<form><input name='username' /><input name='password' /></form>"

    sys.stdout.write("Calling: " + JIRA_URL + "\n")
    jira = requests.get(JIRA_URL).json()

    result = check_pr_against_ticket(
        jira["summary"],
        jira["acceptance_criteria"],
        pr_summary,
        code_diff
    )

    print("LLM Feedback:\n", result)

if __name__ == "__main__":
    main()
