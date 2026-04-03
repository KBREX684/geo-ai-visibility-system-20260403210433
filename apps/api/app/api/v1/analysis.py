from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AnalysisResult, Client, PlatformResponse, TrackingReport
from app.schemas.analysis import AnalysisJobRequest, RecomputeRequest
from app.services.analysis_engine import build_evidence_item, detect_brand_rank, detect_sentiment
from app.services.compliance import DEFAULT_DISCLAIMER
from app.services.orchestrator import OrchestratorAgent
from app.services.score_engine import compute_geo_score

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/jobs")
def create_analysis_job(payload: AnalysisJobRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    client = db.get(Client, payload.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    responses = db.query(PlatformResponse).filter(PlatformResponse.client_id == payload.client_id).all()
    orchestrator = OrchestratorAgent(db)
    job = orchestrator.create_job("analysis", payload.model_dump())
    created = 0
    for response in responses:
        rank = detect_brand_rank(response.response_text, client.brand_name)
        sentiment = detect_sentiment(response.response_text, client.brand_name)
        evidence = build_evidence_item(response.platform, response.prompt_text, response.response_text)
        item = AnalysisResult(
            client_id=payload.client_id,
            response_id=response.id,
            brand_mentioned=1 if rank > 0 else 0,
            brand_rank=rank,
            sentiment=sentiment,
            accuracy_score=0.85 if rank > 0 else 0.65,
            competitor_mentions=[],
            evidence_items=[evidence],
            hallucination_note="",
        )
        db.add(item)
        created += 1
    db.commit()

    analysis_items = [
        {
            "brand_mentioned": bool(x.brand_mentioned),
            "brand_rank": x.brand_rank,
            "sentiment": x.sentiment,
            "accuracy_score": x.accuracy_score,
        }
        for x in db.query(AnalysisResult).filter(AnalysisResult.client_id == payload.client_id).all()
    ]
    score = compute_geo_score(analysis_items)
    report = TrackingReport(
        client_id=payload.client_id,
        period="baseline",
        geo_score_total=score["total"],
        score_breakdown=score,
        delta_vs_baseline=0,
        evidence_summary=[{"total_analysis_items": len(analysis_items)}],
        disclaimer_text=DEFAULT_DISCLAIMER,
        next_actions=["补齐官网FAQ", "增加第三方平台品牌提及内容"],
    )
    db.add(report)
    db.commit()

    orchestrator.mark_success(job.id, {"analysis_created": created, "geo_score": score["total"]})
    return {"job_id": job.id, "status": "success", "analysis_created": created, "score": score}


@router.post("/recompute")
def recompute_scores(payload: RecomputeRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = db.query(TrackingReport).filter(TrackingReport.client_id == payload.client_id).all()
    if not reports:
        raise HTTPException(status_code=404, detail="No reports found")

    analysis_items = [
        {
            "brand_mentioned": bool(x.brand_mentioned),
            "brand_rank": x.brand_rank,
            "sentiment": x.sentiment,
            "accuracy_score": x.accuracy_score,
        }
        for x in db.query(AnalysisResult).filter(AnalysisResult.client_id == payload.client_id).all()
    ]
    recomputed = compute_geo_score(analysis_items)
    for report in reports:
        report.score_breakdown = {**recomputed, "version_note": payload.version_note}
        report.geo_score_total = recomputed["total"]
    db.commit()
    return {"updated_reports": len(reports), "score": recomputed}

