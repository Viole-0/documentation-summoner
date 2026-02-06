from flask import Flask, request, jsonify
from github import Github, GithubIntegration
import os
import requests
from dotenv import load_dotenv
from groq import Groq
import re
import ast

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ------------------------------------------------------------
# 🌟 Groq Universal Caller (single model)
# ------------------------------------------------------------
def call_groq(prompt, max_tokens=350):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


# ------------------------------------------------------------
# 🌙 Title Extractor
# ------------------------------------------------------------
def extract_title(text):
    match = re.search(r'TITLE:\s*"([^"]+)"', text)
    if match:
        return match.group(1).strip()
    return None


# ------------------------------------------------------------
# 🏷 Label Extractor
# ------------------------------------------------------------
def extract_labels(summary_text):
    match = re.search(r'LABELS:\s*(\[.*?\])', summary_text)
    if match:
        try:
            labels = ast.literal_eval(match.group(1))
            if isinstance(labels, list):
                return labels
        except:
            return []
    return []


# ------------------------------------------------------------
# 🌐 Webhook
# ------------------------------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    action = payload.get("action")

    # Slash commands
    if payload.get("comment"):
        handle_comment_command(payload)
        return jsonify({"status": "ok"}), 200

    # PR events
    if payload.get("pull_request") and action in ["opened", "synchronize"]:
        owner = payload["repository"]["owner"]["login"]
        repo_name = payload["repository"]["name"]
        pr_number = payload["pull_request"]["number"]
        installation_id = payload["installation"]["id"]

        # Authenticate
        integration = GithubIntegration(
            os.getenv("GITHUB_APP_ID"),
            open("private-key.pem", "r").read()
        )
        access_token = integration.get_access_token(installation_id).token
        github = Github(access_token)

        repo = github.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(pr_number)

        # Get diff
        diff_text = requests.get(pr.diff_url).text

        # Generate summary
        summary = generate_summary(diff_text)
        pr.create_issue_comment(summary)

        # Auto-label
        labels = extract_labels(summary)
        if labels:
            pr.add_to_labels(*labels)

        # Auto-update PR title
        title = extract_title(summary)
        if title:
            pr.edit(title=title)

    return jsonify({"status": "ok"}), 200


# ------------------------------------------------------------
# 🔥 Slash Command Handler
# ------------------------------------------------------------
def handle_comment_command(payload):
    comment_body = payload["comment"]["body"].strip()
    pr = get_pr_from_payload(payload)

    if not comment_body.startswith("/summon"):
        return

    parts = comment_body.split()
    if len(parts) < 2:
        pr.create_issue_comment("🧙 Summoner says: Provide a command like `/summon summary`")
        return

    command = parts[1].lower()
    diff_text = requests.get(pr.diff_url).text

    if command == "summary":
        response = generate_summary(diff_text)
    elif command == "explain":
        response = generate_explanation(diff_text)
    elif command == "risks":
        response = generate_risk_analysis(diff_text)
    elif command == "title":
        response = generate_title(diff_text)
        suggested = extract_title(response)
        if suggested:
            pr.edit(title=suggested)
    elif command == "labels":
        response = generate_label_suggestions(diff_text)
    else:
        response = f"🧙 Unknown command: `{command}`"

    pr.create_issue_comment(response)


# ------------------------------------------------------------
# 🧿 Get PR from comment payload
# ------------------------------------------------------------
def get_pr_from_payload(payload):
    owner = payload["repository"]["owner"]["login"]
    repo_name = payload["repository"]["name"]
    pr_number = payload["issue"]["number"]
    installation_id = payload["installation"]["id"]

    integration = GithubIntegration(
        os.getenv("GITHUB_APP_ID"),
        open("private-key.pem", "r").read()
    )
    access_token = integration.get_access_token(installation_id).token
    github = Github(access_token)

    repo = github.get_repo(f"{owner}/{repo_name}")
    return repo.get_pull(pr_number)


# ------------------------------------------------------------
# 🌟 Main Summary Generator
# ------------------------------------------------------------
def generate_summary(diff_text):
    prompt = f"""
You are an expert GitHub code reviewer.

Provide a structured summary:

## 🧙 Documentation Summoner — PR Review Summary

### ✨ Suggested PR Title
TITLE: "<your-suggested-title>"

### 📄 Overview

### 🔍 Key Changes

### 🤔 Why It Matters

### 🎯 Impact Level
🟢 Low / 🟡 Medium / 🔴 High

### 🏷️ Suggested Labels
LABELS: ["label1", "label2"]

---

Diff:
{diff_text}
"""
    return call_groq(prompt, max_tokens=600)


# ------------------------------------------------------------
# Additional Summon Abilities
# ------------------------------------------------------------
def generate_explanation(diff_text):
    prompt = f"""
Explain this PR in simple language.

Diff:
{diff_text}
"""
    return call_groq(prompt)


def generate_risk_analysis(diff_text):
    prompt = f"""
Analyze the risk of this PR (Low, Medium, High) and explain why.

Diff:
{diff_text}
"""
    return call_groq(prompt)


def generate_title(diff_text):
    prompt = f"""
Generate a concise PR title.

TITLE: "<your-suggested-title>"

Diff:
{diff_text}
"""
    return call_groq(prompt, max_tokens=60)


def generate_label_suggestions(diff_text):
    prompt = f"""
Suggest 1–3 GitHub labels.

LABELS: ["label1", "label2"]

Diff:
{diff_text}
"""
    return call_groq(prompt)


# ------------------------------------------------------------
# 🚀 Server
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
