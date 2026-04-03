from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import TrackingReport
from app.schemas.reports import ComplianceCheckRequest, TrackingJobRequest
from app.services.compliance import DEFAULT_DISCLAIMER, check_report_compliance

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/tracking")
def create_tracking_report(payload: TrackingJobRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    baseline = (
        db.query(TrackingReport)
        .filter(TrackingReport.client_id == payload.client_id)
        .order_by(TrackingReport.id.desc())
        .first()
    )
    if not baseline:
        raise HTTPException(status_code=404, detail="No baseline report found")

    report = TrackingReport(
        client_id=payload.client_id,
        period=payload.period,
        geo_score_total=baseline.geo_score_total,
        score_breakdown=baseline.score_breakdown,
        delta_vs_baseline=0,
        evidence_summary=baseline.evidence_summary,
        disclaimer_text=DEFAULT_DISCLAIMER,
        next_actions=["持续内容发布", "更新官网结构化数据", "复查竞品提及变化"],
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"report_id": report.id}


@router.post("/compliance-check")
def compliance_check(payload: ComplianceCheckRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(TrackingReport).filter(TrackingReport.client_id == payload.client_id)
    if payload.report_id:
        report = query.filter(TrackingReport.id == payload.report_id).first()
    else:
        report = query.order_by(TrackingReport.id.desc()).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return check_report_compliance(
        {
            "disclaimer_text": report.disclaimer_text,
            "evidence_summary": report.evidence_summary,
            "score_breakdown": report.score_breakdown,
            "next_actions": report.next_actions,
        }
    )


@router.get("/{client_id}")
def get_reports(client_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = db.query(TrackingReport).filter(TrackingReport.client_id == client_id).order_by(TrackingReport.id.desc()).all()
    return [
        {
            "id": report.id,
            "period": report.period,
            "geo_score_total": report.geo_score_total,
            "score_breakdown": report.score_breakdown,
            "delta_vs_baseline": report.delta_vs_baseline,
            "created_at": report.created_at,
        }
        for report in reports
    ]

