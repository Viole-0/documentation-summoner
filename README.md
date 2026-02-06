# 🧙 Documentation Summoner  
### AI-Powered Pull Request Reviewer, Labeler & Title Generator

Documentation Summoner is a GitHub App that automates and enhances Pull Request reviews with AI.  
It reads PR diffs, understands the changes, and responds with structured, human-readable insights.

---

## 🌟 Features

### ✔ Automatic PR Summaries  
Each time a PR is opened or updated, Summoner posts:

- 🧾 Overview  
- 🔍 Key changes  
- 🎯 Impact level (Low/Medium/High)  
- 🏷 Suggested labels  
- ✨ AI-generated PR title  
- 📄 Beautiful formatting  

---

### ✔ Slash Commands  
Interact with the Summoner directly inside PR comments:

```
/summon summary
/summon explain
/summon risks
/summon labels
/summon title
```

---

### ✔ Auto Labeling  
Summoner intelligently categorizes PRs with labels such as:

- documentation  
- enhancement  
- refactor  
- bugfix  
- low-risk / medium-risk / high-impact  

---

### ✔ Auto PR Title Generation  
Suggests clean, professional PR titles —  
and can update the PR title automatically.

---

### ✔ Groq LLM Powered  
Uses a single stable model for reliability:

- `llama-3.3-70b-versatile`  

Provides fast, accurate, and consistent code analysis.

---

## ⚡ Architecture

```
GitHub App → Pull Request Event  
           → Flask Server (Render)  
           → Groq AI Model  
           → GitHub API (comments, labels, titles)
```

---

## 🚀 Getting Started

### 1. Create a GitHub App  
- Permissions:
  - Pull Requests → Read & Write  
  - Issues → Read & Write  
- Events:
  - pull_request  
  - issue_comment  
- Webhook:
  ```
  https://documentation-summoner.onrender.com/webhook
  ```

---

### 2. Environment Variables
```
GITHUB_APP_ID=your_app_id
GROQ_API_KEY=your_groq_api_key
```

### 3. Place your private key  
File must be named:
```
private-key.pem
```

---

## 💻 Running Locally

```
pip install -r requirements.txt
python app.py
```

Server runs at:
```
http://localhost:3000/webhook
```

---

## 📦 Deploying on Render  
1. Create a Web Service  
2. Add environment variables  
3. Connect your GitHub repo  
4. Deploy  
5. Paste Render webhook URL into GitHub App  

---

## 🧪 Testing the App

1. Create a branch  
2. Make a small change  
3. Open a Pull Request  
4. Summoner posts automatic summary  
5. Try slash commands in PR  

---

## 🛣️ Roadmap  

- Inline code comments  
- File-by-file summaries  
- Advanced risk scoring  
- Dashboard analytics  
- GitHub Marketplace launch ✔ (in progress)

---

## 🪄 Author  
Built with curiosity, patience, and late-night energy by **Viole-0**.

---

## 📜 License  
MIT License — free to use, modify, and enhance.

---
