from flask import Flask, request, jsonify
from github import Github, GithubIntegration
import os
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    action = payload.get("action")

    # Only handle PR opened or updated
    if payload.get("pull_request") and action in ["opened", "synchronize"]:
        owner = payload["repository"]["owner"]["login"]
        repo_name = payload["repository"]["name"]
        pr_number = payload["pull_request"]["number"]
        installation_id = payload["installation"]["id"]

        # Authenticate using GitHub App credentials
        integration = GithubIntegration(
            os.getenv("GITHUB_APP_ID"),
            open("private-key.pem", "r").read()
        )

        access_token = integration.get_access_token(installation_id).token
        github = Github(access_token)

        repo = github.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(pr_number)

        # Get diff content
        diff_url = pr.diff_url
        diff_text = requests.get(diff_url).text

        # Generate AI summary
        summary = generate_summary(diff_text)

        # Post summary as PR comment
        pr.create_issue_comment(
            f"🧙 **Documentation Summoner speaks:**\n\n{summary}"
        )

    return jsonify({"status": "ok"}), 200


def generate_summary(diff_text):
    prompt = f"""
    You are an expert software reviewer.
    Summarize the following Pull Request diff clearly and concisely.
    Explain what changed, why it matters, and its potential impact.

    Diff:
    {diff_text}
    """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
