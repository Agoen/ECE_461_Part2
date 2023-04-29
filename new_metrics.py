import requests

# Authentication token (replace with your own token)
token = "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"

def code_review_ratio(owner, repo):
    reviewed_lines = 0
    total_lines = 0
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    print(api_url)

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
        print(f"Fraction of code introduced through pull requests with a code review: {fraction_reviewed}")
    else:
        print("No pull requests found.")
