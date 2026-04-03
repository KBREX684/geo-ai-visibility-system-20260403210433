from pydantic import BaseModel


class AnalysisJobRequest(BaseModel):
    client_id: int


class RecomputeRequest(BaseModel):
    client_id: int
    version_note: str = "score formula update"

