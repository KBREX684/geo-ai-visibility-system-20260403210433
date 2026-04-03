from fastapi import APIRouter

from app.api.v1.analysis import router as analysis_router
from app.api.v1.auth import router as auth_router
from app.api.v1.clients import router as clients_router
from app.api.v1.content import router as content_router
from app.api.v1.diagnostics import router as diagnostics_router
from app.api.v1.ops import router as ops_router
from app.api.v1.reports import router as reports_router
from app.api.v1.tasks import router as tasks_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(clients_router)
api_router.include_router(diagnostics_router)
api_router.include_router(analysis_router)
api_router.include_router(content_router)
api_router.include_router(ops_router)
api_router.include_router(reports_router)
api_router.include_router(tasks_router)

