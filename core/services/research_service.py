import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


class ResearchService:
    """Handles real-time research using Tavily."""

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("TAVILY_API_KEY is not configured.")

        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 6) -> str:
        """Search Tavily and return formatted source information."""

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        response = self.client.search(
            query=query.strip(),
            max_results=max_results,
            topic="general",
        )

        results = response.get("results", [])

        if not results:
            return f"No recent updates found on '{query}'."

        summaries = []

        for result in results:
            title = result.get("title", "")
            content = result.get("content", result.get("snippet", ""))
            url = result.get("url", "")

            summaries.append(
                f"**{title}**\n\n"
                f"{content}\n\n"
                f"Source: {url}"
            )

        return "\n\n----\n\n".join(summaries)


research_service = ResearchService()