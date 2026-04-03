from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Client
from app.schemas.client import ClientCreate, ClientOut

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientOut)
def create_client(payload: ClientCreate, _: str = Depends(get_current_user), db: Session = Depends(get_db)):
    count = db.query(Client).count() + 1
    client = Client(
        client_code=f"CLT-{count:05d}",
        brand_name=payload.brand_name,
        industry=payload.industry,
        city=payload.city,
        core_services=payload.core_services,
        target_persona=payload.target_persona,
        competitors=payload.competitors,
        website_url=payload.website_url,
        social_accounts=payload.social_accounts,
        pain_points=payload.pain_points,
        promise_scope=payload.promise_scope,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

