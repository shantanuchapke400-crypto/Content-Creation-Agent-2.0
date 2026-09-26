"""CreatorOS AI MCP server.

This server exposes the current CreatorOS FastAPI capabilities through MCP.
It talks to the authenticated API instead of importing the legacy Streamlit app.

Environment variables:
    CREATOROS_API_URL  API base URL, default: http://127.0.0.1:8000/api
    CREATOROS_API_TOKEN  JWT access token used by MCP tools
    MCP_TRANSPORT  stdio (default) or streamable-http
"""

import os
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP


API_BASE_URL = os.getenv(
    "CREATOROS_API_URL",
    "http://127.0.0.1:8001/api",
).rstrip("/")
API_TOKEN = os.getenv("CREATOROS_API_TOKEN", "")

mcp = FastMCP("CreatorOS MCP Server")


def _headers() -> dict[str, str]:
    if not API_TOKEN:
        raise RuntimeError(
            "CREATOROS_API_TOKEN is not configured. "
            "Set it to a valid CreatorOS JWT access token."
        )
    return {"Authorization": f"Bearer {API_TOKEN}"}


def _request(
    method: str,
    path: str,
    **kwargs: Any,
) -> Any:
    response = requests.request(
        method,
        f"{API_BASE_URL}{path}",
        headers=_headers(),
        timeout=120,
        **kwargs,
    )

    try:
        payload = response.json()
    except ValueError:
        payload = {"detail": response.text}

    if not response.ok:
        detail = payload.get("detail", payload) if isinstance(payload, dict) else payload
        raise RuntimeError(f"CreatorOS API {response.status_code}: {detail}")

    return payload


def _generate(
    project_id: int,
    content_type: str,
    topic: str = "",
    tone: str = "Professional",
    input_content: str = "",
) -> str:
    payload = _request(
        "POST",
        f"/projects/{project_id}/generations",
        json={
            "content_type": content_type,
            "topic": topic,
            "tone": tone,
            "input_content": input_content,
        },
    )
    generation = payload.get("generation", payload)
    return generation.get("output_content", str(generation))


@mcp.tool(description="Generate a professional blog post for a CreatorOS project.")
def generate_blog(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "blog", topic, tone)


@mcp.tool(description="Generate a LinkedIn post for a CreatorOS project.")
def generate_linkedin_post(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "linkedin", topic, tone)


@mcp.tool(description="Generate a YouTube script for a CreatorOS project.")
def generate_youtube_script(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "youtube", topic, tone)


@mcp.tool(description="Generate an Instagram caption for a CreatorOS project.")
def generate_instagram_caption(project_id: int, topic: str, tone: str = "Friendly") -> str:
    return _generate(project_id, "instagram", topic, tone)


@mcp.tool(description="Generate a Twitter/X thread for a CreatorOS project.")
def generate_twitter_thread(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "twitter", topic, tone)


@mcp.tool(description="Generate a newsletter for a CreatorOS project.")
def generate_newsletter(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "newsletter", topic, tone)


@mcp.tool(description="Generate a professional email for a CreatorOS project.")
def generate_email(project_id: int, topic: str, tone: str = "Professional") -> str:
    return _generate(project_id, "email", topic, tone)


@mcp.tool(description="Rewrite existing content for a CreatorOS project.")
def rewrite_content(project_id: int, content: str, tone: str = "Professional") -> str:
    return _generate(project_id, "rewrite", input_content=content, tone=tone)


@mcp.tool(description="Summarize existing content for a CreatorOS project.")
def summarize_content(project_id: int, content: str, tone: str = "Professional") -> str:
    return _generate(project_id, "summarize", input_content=content, tone=tone)


@mcp.tool(description="Expand existing content for a CreatorOS project.")
def expand_content(project_id: int, content: str, tone: str = "Professional") -> str:
    return _generate(project_id, "expand", input_content=content, tone=tone)


@mcp.tool(description="Humanize existing content for a CreatorOS project.")
def humanize_content(project_id: int, content: str, tone: str = "Friendly") -> str:
    return _generate(project_id, "humanize", input_content=content, tone=tone)


@mcp.tool(description="Generate an SEO title for a CreatorOS project.")
def generate_seo_title(project_id: int, topic: str) -> str:
    return _generate(project_id, "seo_title", topic)


@mcp.tool(description="Generate an SEO meta description for a CreatorOS project.")
def generate_meta_description(project_id: int, topic: str) -> str:
    return _generate(project_id, "meta_description", topic)


@mcp.tool(description="List saved generations for a CreatorOS project.")
def list_generations(project_id: int) -> Any:
    payload = _request("GET", f"/projects/{project_id}/generations")
    return payload.get("generations", payload)


@mcp.tool(description="Open one saved CreatorOS generation by project and generation ID.")
def get_generation(project_id: int, generation_id: int) -> Any:
    payload = _request(
        "GET",
        f"/projects/{project_id}/generations/{generation_id}",
    )
    return payload.get("generation", payload)


@mcp.tool(description="Delete one saved CreatorOS generation.")
def delete_generation(project_id: int, generation_id: int) -> str:
    _request(
        "DELETE",
        f"/projects/{project_id}/generations/{generation_id}",
    )
    return f"Generation {generation_id} deleted successfully."


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()

    if transport not in {"stdio", "streamable-http"}:
        raise ValueError(
            "MCP_TRANSPORT must be 'stdio' or 'streamable-http'."
        )

    mcp.run(transport=transport)