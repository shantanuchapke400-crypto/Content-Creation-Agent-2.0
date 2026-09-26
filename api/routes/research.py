from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core import django_setup
from core.dependencies.auth import get_current_user
from core.services.research_service import research_service
from creator.models import Project, Research


router = APIRouter()


class ResearchRequest(BaseModel):
    query: str
    max_results: int = 6


@router.post("/projects/{project_id}/research")
def create_research(
    project_id: int,
    request: ResearchRequest,
    current_user=Depends(get_current_user),
):
    try:
        if request.max_results < 1 or request.max_results > 10:
            raise HTTPException(
                status_code=400,
                detail="max_results must be between 1 and 10.",
            )

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

        results = research_service.search(
            request.query,
            max_results=request.max_results,
        )

        research = Research.objects.create(
            project=project,
            query=request.query,
            results=results,
        )

        return {
            "status": "success",
            "research": {
                "id": research.id,
                "project_id": research.project_id,
                "query": research.query,
                "results": research.results,
                "created_at": research.created_at,
            },
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )