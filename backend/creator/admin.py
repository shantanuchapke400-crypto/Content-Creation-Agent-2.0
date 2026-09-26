from django.contrib import admin

from .models import Generation, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "updated_at")
    search_fields = ("name", "user__username")


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ("content_type", "project", "tone", "created_at")
    list_filter = ("content_type", "tone")
    search_fields = ("topic", "output_content")
