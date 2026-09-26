from django.conf import settings
from django.db import models


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Generation(models.Model):
    CONTENT_TYPES = [
        ("blog", "Blog"),
        ("linkedin", "LinkedIn Post"),
        ("youtube", "YouTube Script"),
        ("instagram", "Instagram Caption"),
        ("twitter", "Twitter/X Thread"),
        ("newsletter", "Newsletter"),
        ("email", "Email"),
        ("rewrite", "Rewrite"),
        ("summarize", "Summarize"),
        ("expand", "Expand"),
        ("humanize", "Humanize"),
        ("seo_title", "SEO Title"),
        ("meta_description", "Meta Description"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="generations",
    )
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_TYPES,
    )
    topic = models.TextField()
    tone = models.CharField(max_length=50, blank=True)
    input_content = models.TextField(blank=True)
    output_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} - {self.topic[:50]}"


class Research(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="research",
    )
    query = models.TextField()
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query    