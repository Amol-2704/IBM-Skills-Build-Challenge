from fastapi import APIRouter, HTTPException
from app.schemas.investigation import (InvestigationRequest, InvestigationResult)
from app.services.investigation_service import investigation_service



router = APIRouter(
    prefix="/investigate",
    tags=["Investigation"]
)


@router.post("", response_model=InvestigationResult)
def investigate(request: InvestigationRequest):
    try:
        return investigation_service.investigate(
            query=request.query,
            time_range=request.time_range
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
