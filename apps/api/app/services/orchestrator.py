from sqlalchemy.orm import Session

from app.models import AuditLog, Job
from app.services.model_router import pick_model


class OrchestratorAgent:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, task_type: str, payload: dict) -> Job:
        selected_model = pick_model(task_type)
        job = Job(task_type=task_type, payload={**payload, "selected_model": selected_model}, status="queued")
        self.db.add(job)
        self.db.flush()
        self.log(job.id, "job_created", {"task_type": task_type, "selected_model": selected_model})
        self.db.commit()
        self.db.refresh(job)
        return job

    def mark_running(self, job_id: int):
        job = self.db.get(Job, job_id)
        if not job:
            return
        job.status = "running"
        self.log(job_id, "job_running", {})
        self.db.commit()

    def mark_success(self, job_id: int, result: dict):
        job = self.db.get(Job, job_id)
        if not job:
            return
        job.status = "success"
        job.result = result
        self.log(job_id, "job_success", result)
        self.db.commit()

    def mark_failed(self, job_id: int, error: str):
        job = self.db.get(Job, job_id)
        if not job:
            return
        job.status = "failed"
        job.error = error
        self.log(job_id, "job_failed", {"error": error})
        self.db.commit()

    def log(self, job_id: int | None, action: str, detail: dict):
        self.db.add(AuditLog(job_id=job_id, action=action, detail=detail))
        self.db.flush()
