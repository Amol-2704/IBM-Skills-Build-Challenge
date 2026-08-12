from fastapi import APIRouter
from app.schemas.investigation import (InvestigationRequest, InvestigationResult)
from app.services.investigation_service import investigation_service



router = APIRouter(
    prefix="/investigate",
    tags=["Investigation"]
)


@router.post("", response_model=InvestigationResult)
def investigate(request: InvestigationRequest):

    return investigation_service.investigate(
        query=request.query,
        time_range=request.time_range
    )