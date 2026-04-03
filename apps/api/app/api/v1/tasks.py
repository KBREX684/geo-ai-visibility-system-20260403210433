from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Job

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}")
def get_task(task_id: int, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    job = db.get(Job, task_id)
    if not job:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": job.id,
        "task_type": job.task_type,
        "status": job.status,
        "payload": job.payload,
        "result": job.result,
        "error": job.error,
        "updated_at": job.updated_at,
    }

