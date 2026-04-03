from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Client, ContentAsset
from app.schemas.content import ContentJobRequest
from app.services.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/jobs")
def generate_content(payload: ContentJobRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    orchestrator = OrchestratorAgent(db)
    job = orchestrator.create_job("content_generation", payload.model_dump())
    per_platform = max(1, payload.monthly_target // max(1, len(payload.platforms)))
    created = 0
    for platform in payload.platforms:
        for idx in range(per_platform):
            db.add(
                ContentAsset(
                    client_id=payload.client_id,
                    platform=platform,
                    topic=f"{client.brand_name} GEO 内容主题 {idx + 1}",
                    draft_text=f"这是为 {platform} 生成的草稿，强调品牌可见性与证据化表达。",
                    quality_status="draft",
                )
            )
            created += 1
    db.commit()
    orchestrator.mark_success(job.id, {"content_created": created})
    return {"job_id": job.id, "created": created}

