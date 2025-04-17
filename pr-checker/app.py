import logging
from flask import Flask, jsonify, request
import requests
import time
import os
from requests.auth import HTTPBasicAuth

# Wait for services to be up (simplified)
time.sleep(5)

app = Flask(__name__)
# Set up logging
app.logger.setLevel(logging.DEBUG)

# Env variables
# Jira
JIRA_ISSUE_ENDPOINT = os.environ['JIRA_ISSUE_ENDPOINT']
JIRA_API_TOKEN_EMAIL = os.environ['JIRA_API_TOKEN_EMAIL']
JIRA_API_TOKEN = os.environ['JIRA_API_TOKEN']
# Github
GITHUB_ENDPOINT = os.environ['GITHUB_ENDPOINT']
GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']

OLLAMA_URL = "http://ollama:11434/api/chat"

# Check with chat if PR matches content of jira.
def check_pr_against_ticket(jira_summary, jira_criteria, pr_summary, code_diff):
    prompt = f"""
Below are two sections: JIRA Ticket (requirements) and Pull Request (implementation).
Please check whether the pull request meet jira requirements? Add reason for the answer
but don't propose solution.
    
JIRA Ticket (requirements):
Summary: {jira_summary}
Acceptance Criteria: {jira_criteria}

Pull Request (implementation):
Summary: {pr_summary}
Code Diff:
{code_diff[:3000]}
"""

    model = os.environ['OLLAMA_MODEL']
    app.logger.info("Using model: %s", model)
    app.logger.debug("Prompt: %s", prompt)

    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })

    app.logger.info("LLM status: %d", response.status_code)

    result = response.json()
    return result["message"]["content"]

# Fetch jira ticket description
def fetch_jira_issue(issue_key):
    url = JIRA_ISSUE_ENDPOINT + issue_key
    app.logger.info("Calling: %s", url)
    auth = HTTPBasicAuth(JIRA_API_TOKEN_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json"
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    result = response.json()
    app.logger.info("Status: %d", response.status_code)
    return {
        "summary": result["fields"]["summary"],
        "description": result["fields"]["description"]
    }

def fetch_pr_diff(pr_project_path):
    url = GITHUB_ENDPOINT + pr_project_path
    app.logger.info("Calling: %s", url)
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    result = response.text
    app.logger.info("Status: %d", response.status_code)
    return result

def fetch_pr_summary(pr_project_path):
    url = GITHUB_ENDPOINT + pr_project_path
    app.logger.info("Calling: %s", url)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    # app.logger.debug("Headers: %s", json.dumps(headers))
    response = requests.request(
        "GET",
        url,
        headers=headers
    )
    result = response.json()
    app.logger.info("Status: %d", response.status_code)
    return result["title"]

@app.route('/api/check-pr')
def get_check_pr():
    jira = request.args.get('jira')
    github = request.args.get('github')
    app.logger.info("Checking [%s] against [%s]", github, jira)

    pr_summary = fetch_pr_summary(github)
    pr_diff = fetch_pr_diff(github)
    jira_details = fetch_jira_issue(jira)

    llm_response = check_pr_against_ticket(
        jira_details["summary"],
        jira_details["description"],
        pr_summary,
        pr_diff
    )

    return jsonify({
        "jira": jira,
        "jira_summary": jira_details["summary"],
        "pr_summary": pr_summary,
        "pr": github,
        "llm_response": llm_response
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)
