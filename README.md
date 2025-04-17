# ai-pr-validator
Tool validating if raise pull request implementation matches jira ticket requirements

# Docker services
| Service    | Purpose                                                                                                                                                                                                                                           |
|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| mock-apis  | Mock implementation of JIRA REST API.                                                                                                                                                                                                             |
| ollama     | Ollama container                                                                                                                                                                                                                                  |
| pr-checker | REST services listening on `5050` with endpoint accepting  `GET /api/check-pr?jira=&github=` where `jira` is a JIRA ticker number e.g. `PROJ-123` and `github` is a GitHub pull request path in a form `ORGANIZATION/REPOSITORY/pulls/PR-NUMBER`. |

# How to use
## With mock APIs
Start services. For mock-apis you do not need email not tokens.
```shell
OLLAMA_MODEL=llama3.2:latest JIRA_ISSUE_ENDPOINT="http://mock-apis:5000/rest/api/2/issue/" GITHUB_ENDPOINT="http://mock-apis:5000/" JIRA_API_TOKEN_EMAIL=empty JIRA_API_TOKEN=empty GITHUB_API_TOKEN=empty docker-compose up --build
```

Make request  
- http://localhost:5050/api/check-pr?github=testorg/testrepo/pulls/1&jira=PROJ-100  
- http://localhost:5050/api/check-pr?github=testorg/testrepo/pulls/1&jira=PROJ-101

## With GitHub and Jira APIs
### Prepare API tokens
#### Jira
Generate token at https://id.atlassian.com/manage-profile/security/api-tokens and save to `~/gh_tokens/jira_token`

#### GitHub
Generate token at https://github.com/settings/personal-access-tokens and save to `~/gh_tokens/gh_read_PRs`  

### Start services

| Env variable         | Description                                      |
|----------------------|--------------------------------------------------|
| OLLAMA_MODEL         | LLM Model                                        |
| JIRA_ISSUE_ENDPOINT  | https://YOUR_ORG.atlassian.net/rest/api/2/issue/ |
| JIRA_API_TOKEN_EMAIL | YOUR EMAIL                                       |
| JIRA_API_TOKEN       | YOUR TOKEN                                       |
| GITHUB_ENDPOINT      | https://api.github.com/repos/                    |
| GITHUB_API_TOKEN     | YOUR TOKEN                                       |

```shell
OLLAMA_MODEL=llama3.2:latest JIRA_ISSUE_ENDPOINT="https://YOUR_ORG.atlassian.net/rest/api/2/issue/" GITHUB_ENDPOINT="https://api.github.com/repos/" JIRA_API_TOKEN_EMAIL=YOUR_MAIL JIRA_API_TOKEN="$(cat ~/gh_tokens/jira_token)" GITHUB_API_TOKEN="$(cat ~/gh_tokens/gh_read_PRs)" docker-compose up --build
```

Make request
- http://localhost:5050/api/check-pr?github=YOUR_ORG/YOUR_REPO/pulls/1&jira=YOUR-PROJECT-123
