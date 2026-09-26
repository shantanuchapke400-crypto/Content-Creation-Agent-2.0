# 🚀 CreatorOS AI

### MCP-Powered AI Content Creation Agent

CreatorOS AI is an AI-powered content creation platform that combines **Google Gemini**, **Tavily real-time web search**, **Streamlit**, and **Model Context Protocol (MCP)** to research topics and generate high-quality content in multiple formats.

It provides a user-friendly web interface while also exposing reusable AI tools through an MCP server.

---

## ✨ Features

### 📝 Multi-Format Content Generation

CreatorOS AI can generate:

- 📰 Blog Posts
- 💼 LinkedIn Posts
- 🎥 YouTube Scripts
- 📸 Instagram Captions
- 🐦 Twitter/X Threads
- 📚 Research Summaries
- 📧 Emails
- 📨 Newsletters
- ✏️ Content Rewriting
- 📝 Content Summarization
- ➕ Content Expansion
- 🧑‍💻 Content Humanization
- 🔍 SEO Titles
- 🌐 Meta Descriptions

### 🌍 Real-Time Research

Uses **Tavily Search** to retrieve current information from the web before generating content.

This helps the agent work with more up-to-date information rather than relying only on the language model's existing knowledge.

### 🤖 Gemini-Powered Generation

Uses Google's **Gemini API** for content generation and transformation.

### 🔌 MCP Server

CreatorOS AI includes a dedicated **MCP server** exposing reusable content-generation tools.

This allows the content-generation capabilities to be consumed by MCP-compatible clients instead of being limited to the Streamlit application.

### 🎨 Modern Web Interface

Built with Streamlit and customized with CSS to provide a modern dark-themed AI workspace.

### 🎯 Multiple Writing Tones

Users can generate content using different tones:

- Professional
- Friendly
- Educational
- Storytelling
- Marketing

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit UI       │
                    │   CreatorOS AI        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Content Pipeline   │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │   Tavily Search  │        │   Google Gemini  │
       │  Real-Time Data  │        │ Content Creation │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                └─────────────┬─────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │   Generated Content  │
                    └──────────────────────┘


             MCP Integration
             
       MCP Client / Compatible Client
                    │
                    ▼
            ┌─────────────────┐
            │   MCP Server    │
            │  mcp_server.py  │
            └────────┬────────┘
                     │
                     ▼
              CreatorOS Tools

## ⚙️ Environment

Copy `.env.example` to `.env` and configure the Gemini, Tavily, PostgreSQL, Django, and JWT secrets.

For local development, run the FastAPI API and Streamlit frontend separately:

```bash
uv run uvicorn api.main:app --reload
uv run streamlit run app.py
```

The optional MCP server uses the same FastAPI backend and requires a valid `CREATOROS_API_TOKEN`.
