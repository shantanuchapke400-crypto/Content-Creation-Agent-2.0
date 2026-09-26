import os

import requests


API_BASE_URL = os.getenv(
    "CREATOROS_API_URL",
    "http://127.0.0.1:8000/api",
).rstrip("/")
REQUEST_TIMEOUT = int(os.getenv("CREATOROS_API_TIMEOUT", "120"))


class APIClient:
    def __init__(self, token: str | None = None):
        self.base_url = API_BASE_URL
        self.token = token

    def set_token(self, token: str):
        self.token = token

    def _headers(self):
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, username: str, password: str):
        return requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

    def register(self, username: str, email: str, password: str):
        return requests.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password},
            timeout=REQUEST_TIMEOUT,
        )

    def get_projects(self):
        return requests.get(
            f"{self.base_url}/projects",
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    def create_project(self, name: str, description: str = ""):
        return requests.post(
            f"{self.base_url}/projects",
            headers=self._headers(),
            json={"name": name, "description": description},
            timeout=REQUEST_TIMEOUT,
        )

    def generate_content(
        self,
        project_id: int,
        content_type: str,
        topic: str = "",
        tone: str = "Professional",
        input_content: str = "",
        research_id: int | None = None,
    ):
        return requests.post(
            f"{self.base_url}/projects/{project_id}/generations",
            headers=self._headers(),
            json={
                "content_type": content_type,
                "topic": topic,
                "tone": tone,
                "input_content": input_content,
                "research_id": research_id,
            },
            timeout=REQUEST_TIMEOUT,
        )

    def get_generations(self, project_id: int):
        return requests.get(
            f"{self.base_url}/projects/{project_id}/generations",
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    def get_generation(self, project_id: int, generation_id: int):
        return requests.get(
            f"{self.base_url}/projects/{project_id}/generations/{generation_id}",
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    def delete_generation(self, project_id: int, generation_id: int):
        return requests.delete(
            f"{self.base_url}/projects/{project_id}/generations/{generation_id}",
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )

    def delete_project(self, project_id: int):
        return requests.delete(
            f"{self.base_url}/projects/{project_id}",
            headers=self._headers(),
            timeout=REQUEST_TIMEOUT,
        )
