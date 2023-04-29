import requests
import os

token = os.environ.get("GITHUB_TOKEN")

def code_review_ratio(owner, repo):
    reviewed_lines = 0
    total_lines = 0
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    response = requests.get(api_url, auth=("token", token))
    pull_requests = response.json()

    for pull_request in pull_requests:
        if pull_request["merge_commit_sha"]:
            pull_url = pull_request["url"]
            pull_response = requests.get(pull_url, auth=("token", token))
            pull_details = pull_response.json()

            additions = pull_details["additions"]
            deletions = pull_details["deletions"]
            total_lines += (additions + deletions)

            reviews_url = pull_details["url"] + "/reviews"
            reviews_response = requests.get(reviews_url, auth=("token", token))
            reviews = reviews_response.json()
            for review in reviews:
                if review["state"] == "APPROVED":
                    reviewed_lines += (additions + deletions)

    if total_lines > 0:
        fraction_reviewed = reviewed_lines / total_lines
        return fraction_reviewed
    else:
        return 0

def pinned_dependency_ratio(dependencies, target_version):
    pinned_count = 0
    for dep in dependencies:
        if target_version in dep and "==" in dep:
            pinned_count += 1
    total_count = len(dependencies)
    if total_count == 0:
        return 1.0
    else:
        return float(pinned_count) / total_count
        