from pydantic import BaseModel


class TrackingJobRequest(BaseModel):
    client_id: int
    period: str


class ComplianceCheckRequest(BaseModel):
    client_id: int
    report_id: int | None = None

