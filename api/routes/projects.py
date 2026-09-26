from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core import django_setup
from core.dependencies.auth import get_current_user
from creator.models import Project


router = APIRouter()


class ProjectCreateRequest(BaseModel):
    name: str
    description: str = ""


class ProjectUpdateRequest(BaseModel):
    name: str
    description: str = ""


@router.post("/projects")
def create_project(
    request: ProjectCreateRequest,
    current_user=Depends(get_current_user),
):
    project = Project.objects.create(
        user=current_user,
        name=request.name,
        description=request.description,
    )

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


@router.get("/projects")
def list_projects(
    current_user=Depends(get_current_user),
):
    projects = Project.objects.filter(
        user=current_user
    ).order_by("-created_at")

    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
            for project in projects
        ]
    }


@router.get("/projects/{project_id}")
def get_project(
    project_id: int,
    current_user=Depends(get_current_user),
):
    try:
        project = Project.objects.get(
            id=project_id,
            user=current_user,
        )
    except Project.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


@router.put("/projects/{project_id}")
def update_project(
    project_id: int,
    request: ProjectUpdateRequest,
    current_user=Depends(get_current_user),
):
    try:
        project = Project.objects.get(
            id=project_id,
            user=current_user,
        )
    except Project.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    project.name = request.name
    project.description = request.description
    project.save()

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
    }


@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user=Depends(get_current_user),
):
    try:
        project = Project.objects.get(
            id=project_id,
            user=current_user,
        )
    except Project.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    project.delete()

    return {
        "message": "Project deleted successfully."
    }