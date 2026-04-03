from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Client, DiagnosticPrompt, PlatformResponse
from app.schemas.diagnostics import DiagnosticJobRequest, ResponseImportRequest
from app.services.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.post("/jobs")
def create_diagnostic_job(payload: DiagnosticJobRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    orchestrator = OrchestratorAgent(db)
    job = orchestrator.create_job("diagnostic", payload.model_dump())
    prompts = [
        ("brand", f"{client.city}有哪些好的{client.industry}机构？"),
        ("brand", f"推荐几个靠谱的{client.industry}品牌"),
        ("decision", f"{client.brand_name}怎么样？值得去吗？"),
    ]
    for platform in payload.platforms:
        for category, text in prompts:
            db.add(
                DiagnosticPrompt(
                    client_id=client.id,
                    category=category,
                    platform=platform,
                    text=text,
                    batch=payload.batch,
                )
            )
    orchestrator.mark_success(job.id, {"generated_prompts": len(prompts) * len(payload.platforms)})
    return {"job_id": job.id, "status": "success"}


@router.post("/responses/import")
def import_platform_responses(payload: ResponseImportRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    inserted = 0
    for item in payload.items:
        db.add(
            PlatformResponse(
                client_id=item.client_id,
                prompt_id=item.prompt_id,
                platform=item.platform,
                prompt_text=item.prompt_text,
                response_text=item.response_text,
                source=item.source,
            )
        )
        inserted += 1
    db.commit()
    return {"inserted": inserted}

