from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HistoricalIncident(BaseModel):
    id: str
    title: str
    description: str
    subsystem: str
    severity: str
    resolution: str | None = None


class Procedure(BaseModel):
    id: str
    title: str
    description: str
    subsystem: str
    steps: list[str] = Field(default_factory=list)


class InvestigationContext(BaseModel):
    anomaly_id: str
    subsystem: str
    severity: str
    mission_phase: str

    telemetry: dict[str, Any]
    recent_events: list[dict[str, Any]] = Field(
        default_factory=list
    )

    historical_incidents: list[HistoricalIncident] = Field(
        default_factory=list
    )

    procedures: list[Procedure] = Field(
        default_factory=list
    )

    generated_at: datetime


class InvestigationRequest(BaseModel):
    query: str
    time_range: str = "24h"


class InvestigationResult(BaseModel):
    investigation_id: str
    query: str
    severity: str
    summary: list[str]
    anomalies: list[Any]
    evidence: list[Any]
    confidence: float
    next_steps: list[str]
