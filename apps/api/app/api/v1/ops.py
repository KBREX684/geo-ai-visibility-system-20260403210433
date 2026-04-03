from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import ContentAsset, PublishSchedule
from app.schemas.ops import OpsScheduleRequest

router = APIRouter(prefix="/ops", tags=["ops"])


@router.post("/schedules")
def create_schedules(payload: OpsScheduleRequest, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    assets = db.query(ContentAsset).filter(ContentAsset.client_id == payload.client_id).all()
    created = 0
    start_at = datetime.now(timezone.utc) + timedelta(days=1)
    for idx, asset in enumerate(assets):
        schedule = PublishSchedule(
            client_id=payload.client_id,
            platform=asset.platform,
            asset_id=asset.id,
            scheduled_at=start_at + timedelta(days=idx),
            status="scheduled",
        )
        db.add(schedule)
        created += 1
    db.commit()
    return {"scheduled_items": created}

