from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any

from app.schemas.investigation import (
    HistoricalIncident,
    InvestigationContext,
    Procedure,
)
from app.core.config import DATA_DIR

class ContextService:
    _SUBSYSTEM_ALIASES = {
        "power": {"power", "battery"},
        "battery": {"power", "battery"},
    }

    def subsystem_matches(self, candidate: str, subsystem: str) -> bool:
        """Match operational terminology used across the small local knowledge base."""
        candidate_key = candidate.strip().lower()
        subsystem_key = subsystem.strip().lower()
        aliases = self._SUBSYSTEM_ALIASES.get(subsystem_key, {subsystem_key})
        return candidate_key in aliases

    def _load_json(self, path: Path) -> Any:

        if not path.exists():
            return []

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_historical_incidents(self) -> list[HistoricalIncident]:

        path = DATA_DIR / "incidents.json"

        data = self._load_json(path)

        if not data:
            return []

        if isinstance(data, dict):
            data = [data]

        return [
            HistoricalIncident(**incident)
            for incident in data
        ]

    def _load_procedures(
        self,
        subsystem: str
    ) -> list[Procedure]:

        path = (
            DATA_DIR
            / "procedures"
            / f"{subsystem.lower()}.json"
        )

        data = self._load_json(path)

        if not data:
            return []

        if isinstance(data, dict):
            data = [data]

        return [
            Procedure(**procedure)
            for procedure in data
        ]

    def build_context(
        self,
        anomaly_id: str,
        telemetry,
        severity: str,
    ) -> InvestigationContext:

        historical_incidents = (
            self._load_historical_incidents()
        )

        procedures = []
        # Procedures may be indexed under an operational alias (Power/Battery).
        for procedure_subsystem in self._SUBSYSTEM_ALIASES.get(
            telemetry.subsystem.lower(), {telemetry.subsystem.lower()}
        ):
            procedures.extend(self._load_procedures(procedure_subsystem))

        telemetry_data = {
            "battery_temperature":
                telemetry.battery_temperature,

            "current_draw":
                telemetry.current_draw,

            "battery_voltage":
                telemetry.battery_voltage,
        }

        recent_events = [
            {
                "timestamp":
                    telemetry.timestamp.isoformat(),

                "type":
                    "TELEMETRY",

                "message":
                    (
                        f"{telemetry.subsystem} telemetry "
                        f"triggered anomaly {anomaly_id}."
                    ),
            }
        ]

        return InvestigationContext(
            anomaly_id=anomaly_id,
            subsystem=telemetry.subsystem,
            severity=severity,
            mission_phase=telemetry.mission_phase,
            telemetry=telemetry_data,
            recent_events=recent_events,
            historical_incidents=historical_incidents,
            procedures=procedures,
            generated_at=datetime.now(timezone.utc),
        )


context_service = ContextService()
