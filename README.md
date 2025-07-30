# 🌐 Web & Reddit Analyzer + AI Chatbot

A powerful open-source web and Reddit analytics suite built with Flask, combining SEO auditing, technical checks, Reddit trend analysis, and AI-assisted insights — all in one.

> Built and maintained by [Mivibzzz.com](https://mivibzzz.com), where we craft **custom solutions** for almost any online challenge. This tool is a public example of the high-impact internal tools we develop and occasionally open-source.

---

## 🔍 Features

- **Website Analyzer**  
  Get comprehensive data on:
  - SEO elements (meta tags, H1s, canonical links)
  - Technical stats (headers, response times, compression)
  - Domain WHOIS info
  - SSL and security header analysis
  - Sitemap & `robots.txt` presence

- **Reddit Analyzer**  
  Automatically searches Reddit for a keyword or phrase, returning:
  - Search results with metadata
  - Sentiment analysis of posts
  - Subreddit frequency breakdown

- **AI Chatbot (local inference)**  
  Sends prompts to a local LLM (e.g., Gemma 12B) for real-time SEO or visibility advice.

- **Built-in Game & Analytics Dashboard**  
  Frontend files (`game.html`, `analytics.html`) can be served for demos or data presentation.

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8+
- `pip` installed
- Local AI inference server (optional, for chatbot)

### 🔧 Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/website-reddit-analyzer.git
    cd website-reddit-analyzer
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the server**:

    ```bash
    python app.py
    ```

4. Open your browser:

    - Game page: [http://localhost:7777/](http://localhost:7777/)
    - Analytics dashboard: [http://localhost:7777/analytics](http://localhost:7777/analytics)

---

## 📡 API Endpoints

### `/api/analyze-website`  
POST JSON:
```json
{ "url": "https://example.com" }


Returns detailed analysis on SEO, tech audit, domain info, and security.
/api/analyze-reddit

POST JSON:

{ "query": "open source tools", "limit": 30 }

Returns Reddit search results, sentiment data, and subreddit distribution.
/api/ai-chat

POST JSON:

{ "message": "Give me SEO tips for my landing page" }

Returns a natural language response from your locally running LLM (e.g., Gemma 12B).

    Note: Requires a local AI server listening at http://127.0.0.1:1234.


🧠 Why Open Source?

This tool is one of the internal components we use at Mivibzzz.com to perform deep digital audits and competitive research for clients across industries. We specialize in:

    Custom-built automations

    Deep SEO & technical audits

    AI-powered online visibility optimization

    End-to-end business intelligence tooling

Want a solution that goes beyond cookie-cutter tools?
📩 Reach out at [Mivibzzz.com](https://mivibzzz.com)
“If it exists on the internet, we can analyze it or automate it.”
