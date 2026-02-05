\# 🧙 Documentation Summoner  

\### AI-Powered Pull Request Reviewer — Summaries • Labels • Risk Analysis • Slash Commands



Documentation Summoner is a GitHub App that reads Pull Requests, analyzes the code changes using AI, and comments automatically with:



\- 📄 Beautifully formatted summaries  

\- 🔍 Key change highlights  

\- 🎯 Impact rating  

\- 🏷️ Auto-suggested labels  

\- ✨ AI-generated PR titles  

\- ⚡ Slash commands (`/summon summary`, `/summon risks`, `/summon title`, etc.)



Powered by Groq LLMs and deployed on Render, it turns every PR into a structured, intelligent review.



---



\## ⚡ Features



\### 🧙 Automated PR Summary  

Every time a PR is opened or updated, the Summoner comments with:



\- Overview  

\- Key changes  

\- Why it matters  

\- Impact level  

\- Suggested labels  

\- Suggested PR title  



---



\### 🏷️ Auto-Labeling  

The bot analyzes the diff and intelligently assigns labels like:



\- `documentation`

\- `enhancement`

\- `refactor`

\- `bugfix`

\- `low-risk`, `medium-risk`, `high-impact`



Auto-labeling helps maintainers triage faster.



---



\### ✨ AI-Powered Title Suggestions  

The bot proposes short, clean, professional PR titles — and can optionally \*\*update the PR title automatically\*\*.



---



\### ⚔️ Slash Commands  

Inside any PR comment, you can summon the bot with:



```

/summon summary

/summon explain

/summon risks

/summon labels

/summon title

```



This makes the bot interactive — perfect for deeper review cycles.



---



\### 🤖 Multi-Model Intelligence  

Different tasks use different Groq models for optimal results:



\- Summaries → 70B model  

\- Titles → 12B model  

\- Explanations → 8B model  

\- Risks → 70B model  

\- Labels → 12B model  



Faster. Smarter. Cost-efficient.



---



\## 🧩 Architecture Overview



```

GitHub App  →  Webhook Event  →  Flask Server (Render)

&nbsp;          →  Groq LLM (analysis)

&nbsp;          →  GitHub API (comments, labels, titles)

```



\- GitHub sends PR + comment events  

\- Flask listens on `/webhook`  

\- Summoner fetches diffs → sends to Groq  

\- Summoner comments back with structured analysis  

\- Summoner optionally modifies PR metadata (labels, title)



---



\## 🚀 Getting Started



\### 1. Create the GitHub App  

\- Set permissions:

&nbsp; - Pull Requests → Read \& Write  

&nbsp; - Issues → Read \& Write  

\- Subscribe to events:

&nbsp; - `pull\_request`

&nbsp; - `issue\_comment`  

\- Add webhook:

&nbsp; ```

&nbsp; https://your-render-url/webhook

&nbsp; ```



\### 2. Environment Variables  

```

GITHUB\_APP\_ID=your\_app\_id

GROQ\_API\_KEY=your\_groq\_key

```



\### 3. Add Your Private Key  

Place `private-key.pem` in the project root.



---



\## 🛠️ Running Locally



```

pip install -r requirements.txt

python app.py

```



App runs at:



```

http://localhost:3000/webhook

```



---



\## 📦 Deploying to Render  

\- Create a new Web Service  

\- Add environment variables  

\- Add `runtime.txt` with Python 3.11  

\- Deploy  

\- Connect your GitHub App webhook to the Render URL



---



\## 🧪 Testing



1\. Create new PR  

2\. Make any edit  

3\. Watch Documentation Summoner comment automatically  

4\. Try a slash command:



```

/summon risks

```



---



\## 🌌 Roadmap



\- \[ ] File-by-file summaries  

\- \[ ] Inline code comments  

\- \[ ] CI/CD integration  

\- \[ ] Support for multiple repos automatically  

\- \[ ] Analytics dashboard (PR complexity, change size)  

\- \[ ] GitHub Marketplace launch  



---



\## 💖 Author  

Created with purpose, patience, and late-night coffee by a developer who loves automation.



You can summon the creator here:  

\*\*Viole-0\*\*



---



\## 🪄 License  

MIT License.  

Use freely. Improve freely. Summon freely.



---



\# ✨ “Documentation is the whisper of understanding —  

and your Summoner has learned to speak.” 



