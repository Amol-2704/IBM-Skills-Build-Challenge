from datetime import datetime
from pydantic import BaseModel

class TelemetryRecord(BaseModel):
    anomaly_id: str
    timestamp: datetime

    subsystem: str
    mission_phase: str

    battery_temperature: float
    current_draw: float
    battery_voltage: float
