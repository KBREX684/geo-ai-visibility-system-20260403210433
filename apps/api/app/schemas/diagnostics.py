from pydantic import BaseModel, Field


class DiagnosticJobRequest(BaseModel):
    client_id: int
    platforms: list[str] = Field(default_factory=lambda: ["chatgpt", "perplexity", "kimi", "deepseek", "google_aio"])
    batch: str = "baseline"


class ResponseImportItem(BaseModel):
    client_id: int
    prompt_id: int
    platform: str
    prompt_text: str
    response_text: str
    source: str = "manual"


class ResponseImportRequest(BaseModel):
    items: list[ResponseImportItem]

