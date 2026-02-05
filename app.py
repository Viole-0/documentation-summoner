from flask import Flask, request, jsonify
from github import Github, GithubIntegration
import os
import requests
from dotenv import load_dotenv
from groq import Groq
import re
import ast
import sqlite3
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ------------------------------------------------------------
# 🌟 MULTI-MODEL ROUTER
# ------------------------------------------------------------
MODEL_MAP = {
    "summary": "llama-3.3-70b-versatile",
    "explanation": "llama-3.1-8b-instant",
    "risk": "llama-3.3-70b-versatile",
    "title": "llama-3.1-12b-instant",
    "labels": "llama-3.1-12b-instant"
}

def call_groq(prompt, mode="summary", max_tokens=350):
    model = MODEL_MAP.get(mode, "llama-3.3-70b-versatile")

    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


# ------------------------------------------------------------
# 🌙 EXTRACT TITLE
# ------------------------------------------------------------
def extract_title(text):
    match = re.search(r'TITLE:\s*"([^"]+)"', text)
    if match:
        return match.group(1).strip()
    return None


# ------------------------------------------------------------
# 🏷 LABEL EXTRACTOR
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
# 🧿 SAVE PR TO DATABASE (Dashboard Logger)
# ------------------------------------------------------------
def save_pr_to_db(pr_number, title, summary, labels, repo):
    conn = sqlite3.connect("dashboard/database.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS pr_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pr_number INTEGER,
            title TEXT,
            summary TEXT,
            labels TEXT,
            repo TEXT,
            timestamp TEXT
        )
    """)

    c.execute("""
        INSERT INTO pr_logs (pr_number, title, summary, labels, repo, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        pr_number,
        title,
        summary,
        ",".join(labels) if labels else "",
        repo,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


# ------------------------------------------------------------
# 🌐 WEBHOOK HANDLER
# ------------------------------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json
    action = payload.get("action")

    # Handle Slash Commands
    if payload.get("comment"):
        handle_comment_command(payload)
        return jsonify({"status": "ok"}), 200

    # Handle PR events (opened or updated)
    if payload.get("pull_request") and action in ["opened", "synchronize"]:
        owner = payload["repository"]["owner"]["login"]
        repo_name = payload["repository"]["name"]
        pr_number = payload["pull_request"]["number"]
        installation_id = payload["installation"]["id"]

        integration = GithubIntegration(
            os.getenv("GITHUB_APP_ID"),
            open("private-key.pem", "r").read()
        )

        access_token = integration.get_access_token(installation_id).token
        github = Github(access_token)

        repo = github.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(pr_number)

        diff_text = requests.get(pr.diff_url).text

        # Summarize PR
        summary = generate_summary(diff_text)
        pr.create_issue_comment(summary)

        # Auto label
        labels = extract_labels(summary)
        if labels:
            pr.add_to_labels(*labels)

        # Auto-update PR title
        title = extract_title(summary)
        if title:
            pr.edit(title=title)

        '''# 🌟 Save PR to dashboard DB
        save_pr_to_db(
            pr_number=pr_number,
            title=title or pr.title,
            summary=summary,
            labels=labels or [],
            repo=f"{owner}/{repo_name}"
        )'''

    return jsonify({"status": "ok"}), 200


# ------------------------------------------------------------
# 🔥 SLASH COMMAND HANDLER
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
# 👁️ GET PR FROM COMMENT PAYLOAD
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
# 🌟 SUMMARY GENERATOR (MAIN FEATURE)
# ------------------------------------------------------------
def generate_summary(diff_text):
    prompt = f"""
You are an expert code reviewer for GitHub Pull Requests.

Read the diff and produce a structured GitHub comment:

## 🧙 Documentation Summoner — PR Review Summary

### ✨ Suggested PR Title
(A short, clear title summarizing the change)
TITLE: "<your-suggested-title>"

### 📄 Overview
(2–4 sentence summary)

### 🔍 Key Changes
(Bullet list of 3–6 items)

### 🤔 Why It Matters
(Short explanation)

### 🎯 Impact Level
🟢 Low, 🟡 Medium, or 🔴 High

### 🏷️ Suggested Labels
LABELS: ["label1", "label2"]

---

Diff:
{diff_text}
"""
    return call_groq(prompt, mode="summary", max_tokens=600)


# ------------------------------------------------------------
# 🧙 OTHER SUMMON FUNCTIONS
# ------------------------------------------------------------
def generate_explanation(diff_text):
    prompt = f"""
Explain this PR in simple, clear language.

Diff:
{diff_text}
"""
    return call_groq(prompt, mode="explanation")


def generate_risk_analysis(diff_text):
    prompt = f"""
Assess the risk of this PR: Low, Medium, or High.
Explain your reasoning in 3–5 sentences.

Diff:
{diff_text}
"""
    return call_groq(prompt, mode="risk")


def generate_title(diff_text):
    prompt = f"""
Generate a clean, concise GitHub PR title.
10 words max. No emojis.

TITLE: "<your-suggested-title>"

Diff:
{diff_text}
"""
    return call_groq(prompt, mode="title", max_tokens=50)


def generate_label_suggestions(diff_text):
    prompt = f"""
Suggest 1–3 GitHub labels for this PR.

LABELS: ["label1", "label2"]

Diff:
{diff_text}
"""
    return call_groq(prompt, mode="labels")


# ------------------------------------------------------------
# 🚀 RUN SERVER
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
