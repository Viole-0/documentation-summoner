# 🧙 Documentation Summoner  
### AI-Powered Pull Request Reviewer, Labeler & Title Generator

Documentation Summoner is a GitHub App that enhances Pull Request workflows using AI.  
It reads your PR diffs, understands the changes, and responds with structured, human-quality insights.

---

## 🌟 What Documentation Summoner Does

### ✔ Automatic PR Summaries  
Whenever a PR is opened or updated, the Summoner posts:

- A clean, multi-section summary  
- Key change breakdown  
- Why the change matters  
- Impact rating (Low / Medium / High)  
- Recommended labels  
- AI-generated PR title  

---

### ✔ Slash Commands (Interactive)  
Inside any PR comment, you can summon the bot directly:

```
/summon summary
/summon explain
/summon risks
/summon labels
/summon title
```

It will instantly respond with the requested analysis.

---

### ✔ Auto-Labeling  
Summoner extracts the nature of the change and applies labels such as:

- documentation  
- enhancement  
- refactor  
- bugfix  
- low-risk / medium-risk / high-impact  

---

### ✔ AI-Generated PR Titles  
The bot suggests clean, professional titles based on the diff.  
It can even **edit the PR title automatically** using the machine-readable output.

---

### ✔ Multi-Model AI Pipeline  
Different features use optimal Groq models:

- Summaries → 70B  
- Risks → 70B  
- Titles → 12B  
- Explanations → 8B  
- Labels → 12B  

This keeps the app fast, cost-efficient, and sharp.

---

## ⚡ Architecture

```
GitHub App → PR Event → Flask Webhook (Render)
          → Groq LLM → Summarization / Labels / Titles
          → GitHub API → Comment + Update PR Metadata
```

---

## 🚀 Getting Started (Setup Guide)

1. Create a GitHub App  
2. Enable permissions:  
   - Pull Requests: Read & Write  
   - Issues: Read & Write  
3. Subscribe to events:  
   - pull_request  
   - issue_comment  
4. Add webhook:  
   ```
   https://your-render-url/webhook
   ```  
5. Add environment variables:  
   ```
   GITHUB_APP_ID=xxx
   GROQ_API_KEY=xxx
   ```
6. Add your GitHub App private key as `private-key.pem`  

---

## 💻 Deploy on Render

1. Create a Web Service  
2. Connect repo: `documentation-summoner`  
3. Add env vars  
4. Deploy  
5. Update Webhook URL in GitHub App  

---

## 🧪 Testing

1. Create a branch  
2. Make a small change  
3. Open pull request  
4. Summoner comments automatically  
5. Run slash commands to interact  

---

## 🛣️ Roadmap

- Inline code review comments  
- File-by-file summaries  
- Dashboard + analytics  
- Multi-repo auto-installation  
- GitHub Marketplace listing  

---

## 🪄 Author  
Crafted with patience, curiosity, and a little magic by **Viole-0**.

---

## 📜 License  
MIT License — free to use, modify, and enhance.

