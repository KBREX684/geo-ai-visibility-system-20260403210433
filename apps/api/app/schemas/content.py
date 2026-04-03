from pydantic import BaseModel, Field


class ContentJobRequest(BaseModel):
    client_id: int
    platforms: list[str] = Field(default_factory=lambda: ["zhihu", "xiaohongshu"])
    monthly_target: int = 10

