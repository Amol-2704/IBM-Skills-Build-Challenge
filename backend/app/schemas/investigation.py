from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HistoricalIncident(BaseModel):
    id: str
    title: str
    subsystem: str
    description: str


class Procedure(BaseModel):
    id: str
    title: str
    subsystem: str
    steps: list[str]


class InvestigationRequest(BaseModel):
    anomaly_id: str = Field(..., min_length=1)


class InvestigationContext(BaseModel):
    anomaly_id: str
    subsystem: str
    severity: str
    mission_phase: str

    telemetry: dict[str, Any]
    recent_events: list[dict[str, Any]]

    historical_incidents: list[HistoricalIncident]
    procedures: list[Procedure]

    generated_at: datetime
    