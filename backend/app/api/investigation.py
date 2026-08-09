from app.context.context_service import context_service
from fastapi import APIRouter, HTTPException

from app.schemas.investigation import (
    InvestigationContext,
    InvestigationRequest,
)


router = APIRouter(
    prefix="/api",
    tags=["Investigation"],
)


@router.post(
    "/investigate",
    response_model=InvestigationContext,
)
def investigate(
    request: InvestigationRequest,
):
    try:
        return context_service.build_context(
            request.anomaly_id
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Investigation failed: {error}",
        )