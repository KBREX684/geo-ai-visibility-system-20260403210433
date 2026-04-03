from pydantic import BaseModel


class OpsScheduleRequest(BaseModel):
    client_id: int

