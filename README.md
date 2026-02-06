# 3CX BigQuery SQL Agent

A Python agent powered by **Google Gemini** & **Google ADK** that queries BigQuery data using natural language. Sign in with Google, pick any project you have access to, and start querying — no pre-configuration needed.

## Features

- 🔐 **Google OAuth Login** — Sign in via browser, access any project in your account
- 🗣️ **Natural Language Queries** — Ask questions in plain English, get SQL results
- 🤖 **Powered by Gemini 3 Pro** — Google's latest LLM for intelligent query generation
- 🔧 **Google ADK Integration** — Built with Google's Agent Development Kit
- 🌐 **HTML5 Web Interface** — Streaming chat with SSE, tool indicators, token stats
- 🎨 **CLI Also Available** — Original colored terminal interface still works

## Architecture

```
Browser (OAuth token)
  ↓ Bearer token per request
FastAPI Server
  ├─ /api/projects   → Cloud Resource Manager API (list user's projects)
  ├─ /api/datasets   → BigQuery API (list datasets in project)
  └─ /api/query      → ADK Runner → Gemini → BigQuery → SSE stream back
```

The user's Google OAuth token is used for **both** BigQuery access and project discovery. The Gemini API key is server-side only. Credentials never leave the local machine.

## Quick Start

### Prerequisites

- Python 3.10+
- A Google Cloud OAuth Client ID (see Setup)
- A Gemini API key

### Setup

1. **Clone & install**
   ```bash
   git clone https://github.com/yourusername/GoogleBigQueryAgent.git
   cd GoogleBigQueryAgent
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Create an OAuth Client ID**
   - Go to [Google Cloud Console → APIs & Credentials](https://console.cloud.google.com/apis/credentials)
   - Create an **OAuth 2.0 Client ID** (type: Web application)
   - Add `http://localhost:8000` to **Authorized JavaScript origins**
   - Copy the Client ID

3. **Configure**
   ```bash
   cp .env.example .env
   # Edit .env → set GOOGLE_API_KEY
   ```
   Then edit `static/index.html` and replace `__YOUR_OAUTH_CLIENT_ID__` with your Client ID.

4. **Enable APIs** in your Google Cloud project:
   - BigQuery API
   - Cloud Resource Manager API

5. **Run**
   ```bash
   python -m uvicorn server:app --port 8000
   ```
   Open http://localhost:8000 → Sign in → Pick a project → Query.

## How It Works

1. User clicks **Sign in with Google** → browser-side OAuth (implicit flow)
2. App gets an access token with `bigquery.readonly` + `cloud-platform.read-only` scopes
3. User picks a project and optionally a default dataset
4. Each query sends the access token to the FastAPI backend
5. Backend creates an ADK agent with the user's credentials and streams results via SSE

## Example Questions

- "What datasets are available?"
- "Show me the schema of the cdroutput table"
- "Show me all calls that happened yesterday"
- "How many calls did Sarah answer in the last 30 days?"
- "Can you show me all calls in the last 30 days that were abusive or spam related?"

## Project Structure

```
GoogleBigQueryAgent/
├── bigquery_agent/
│   ├── __init__.py       # Package exports
│   ├── agent.py          # LlmAgent factory (accepts OAuth token + project)
│   └── cli.py            # CLI interface (original, uses ADC)
├── static/
│   └── index.html        # Web interface with OAuth login
├── server.py             # FastAPI backend with SSE streaming
├── .env.example          # Environment template
├── main.py               # CLI entry point
├── pyproject.toml        # Package configuration
├── requirements.txt      # Dependencies
└── README.md
```

## CLI (legacy)

The original CLI still works if you have Application Default Credentials configured:

```bash
gcloud auth application-default login
python main.py
```

Note: The CLI uses the old agent interface. You may need to adjust imports if using the updated agent module.

## License

MIT License — see [LICENSE](LICENSE) for details.
