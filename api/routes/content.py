from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core import django_setup
from core.dependencies.auth import get_current_user
from core.exceptions import (
    AIQuotaExceededError,
    AIServiceUnavailableError,
)
from core.services.content_service import content_service
from core.services.generation_service import generation_service
from creator.models import Generation, Project, Research


router = APIRouter()


class ContentRequest(BaseModel):
    topic: str = ""
    content_type: str
    tone: str = "Professional"
    input_content: str = ""
    research_id: int | None = None


@router.post("/projects/{project_id}/generations")
def generate_content(
    project_id: int,
    request: ContentRequest,
    current_user=Depends(get_current_user),
):
    try:
        # Verify project ownership
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

        # Get saved research if research_id was provided
        research = None

        if request.research_id is not None:
            try:
                research = Research.objects.get(
                    id=request.research_id,
                    project=project,
                )
            except Research.DoesNotExist:
                raise HTTPException(
                    status_code=404,
                    detail="Research not found for this project.",
                )

        # Generate content
        if request.content_type == "blog":
            result = content_service.generate_blog(
                request.topic,
                request.tone,
                research.results if research else None,
            )

        elif request.content_type == "linkedin":
            result = content_service.generate_linkedin_post(
                request.topic,
                request.tone,
                research.results if research else None,
            )

        elif request.content_type == "youtube":
            result = content_service.generate_youtube_script(
                request.topic,
                request.tone,
                research.results if research else None,
            )

        elif request.content_type == "instagram":
            result = content_service.generate_instagram_caption(
                request.topic,
                request.tone,
            )

        elif request.content_type == "twitter":
            result = content_service.generate_twitter_thread(
                request.topic,
                request.tone,
            )

        elif request.content_type == "newsletter":
            result = content_service.generate_newsletter(
                request.topic,
                request.tone,
            )

        elif request.content_type == "email":
            result = content_service.generate_email(
                request.topic,
                request.tone,
            )

        elif request.content_type == "rewrite":
            if not request.input_content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="input_content is required for rewrite.",
                )

            result = content_service.rewrite_content(
                request.input_content,
                request.tone,
            )

        elif request.content_type == "summarize":
            if not request.input_content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="input_content is required for summarize.",
                )

            result = content_service.summarize_content(
                request.input_content,
                request.tone,
            )

        elif request.content_type == "expand":
            if not request.input_content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="input_content is required for expand.",
                )

            result = content_service.expand_content(
                request.input_content,
                request.tone,
            )

        elif request.content_type == "humanize":
            if not request.input_content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="input_content is required for humanize.",
                )

            result = content_service.humanize_content(
                request.input_content,
                request.tone,
            )

        elif request.content_type == "seo_title":
            result = content_service.generate_seo_title(
                request.topic,
                request.tone,
            )

        elif request.content_type == "meta_description":
            result = content_service.generate_meta_description(
                request.topic,
                request.tone,
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported content type: {request.content_type}",
            )

        # Save generation
        generation = generation_service.save_generation(
            project_id=project_id,
            content_type=request.content_type,
            topic=request.topic,
            tone=request.tone,
            input_content=request.input_content,
            output_content=result,
        )

        return {
            "status": "success",
            "generation": {
                "id": generation.id,
                "project_id": generation.project_id,
                "content_type": generation.content_type,
                "topic": generation.topic,
                "tone": generation.tone,
                "output_content": generation.output_content,
                "created_at": generation.created_at,
            },
        }

    except HTTPException:
        raise

    except AIServiceUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )

    except AIQuotaExceededError as error:
        raise HTTPException(
            status_code=429,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@router.get("/projects/{project_id}/generations")
def list_generations(
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

    generations = Generation.objects.filter(
        project=project
    ).order_by("-created_at")

    return {
        "project_id": project.id,
        "generations": [
            {
                "id": generation.id,
                "content_type": generation.content_type,
                "topic": generation.topic,
                "tone": generation.tone,
                "input_content": generation.input_content,
                "output_content": generation.output_content,
                "created_at": generation.created_at,
            }
            for generation in generations
        ],
    }


@router.get("/projects/{project_id}/generations/{generation_id}")
def get_generation(
    project_id: int,
    generation_id: int,
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

    try:
        generation = Generation.objects.get(
            id=generation_id,
            project=project,
        )
    except Generation.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Generation not found.",
        )

    return {
        "id": generation.id,
        "project_id": generation.project_id,
        "content_type": generation.content_type,
        "topic": generation.topic,
        "tone": generation.tone,
        "input_content": generation.input_content,
        "output_content": generation.output_content,
        "created_at": generation.created_at,
    }


@router.delete("/projects/{project_id}/generations/{generation_id}")
def delete_generation(
    project_id: int,
    generation_id: int,
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

    try:
        generation = Generation.objects.get(
            id=generation_id,
            project=project,
        )
    except Generation.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Generation not found.",
        )

    generation.delete()

    return {
        "message": "Generation deleted successfully."
    }

