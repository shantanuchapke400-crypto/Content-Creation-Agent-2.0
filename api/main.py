from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.research import router as research_router
from api.routes.content import router as content_router
from api.routes.projects import router as projects_router
from api.routes.auth import router as auth_router


app = FastAPI(
    title="CreatorOS API",
    description="Backend API for CreatorOS AI SaaS",
    version="1.0.0",
)


app.include_router(health_router, prefix="/api")
app.include_router(research_router, prefix="/api")
app.include_router(content_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(auth_router, prefix="/api")







