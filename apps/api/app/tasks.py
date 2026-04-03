from app.celery_app import celery


@celery.task(bind=True, max_retries=2, default_retry_delay=10)
def run_job(self, job_id: int):
    return {"job_id": job_id, "status": "queued_for_background_execution"}

