from core import django_setup

from creator.models import Generation, Project


class GenerationService:
    """Handles persistence of generated CreatorOS content."""

    @staticmethod
    def save_generation(
        project_id: int,
        content_type: str,
        topic: str,
        tone: str,
        output_content: str,
        input_content: str = "",
    ) -> Generation:
        project = Project.objects.get(id=project_id)

        return Generation.objects.create(
            project=project,
            content_type=content_type,
            topic=topic,
            tone=tone,
            input_content=input_content,
            output_content=output_content,
        )


generation_service = GenerationService()
