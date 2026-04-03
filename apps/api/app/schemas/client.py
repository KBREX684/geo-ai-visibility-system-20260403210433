from pydantic import BaseModel, Field


class ClientCreate(BaseModel):
    brand_name: str
    industry: str
    city: str
    core_services: list[str] = Field(default_factory=list)
    target_persona: str = ""
    competitors: list[str] = Field(default_factory=list)
    website_url: str = ""
    social_accounts: list[str] = Field(default_factory=list)
    pain_points: str = ""
    promise_scope: str = "visibility_only"


class ClientOut(ClientCreate):
    id: int
    client_code: str

    class Config:
        from_attributes = True

