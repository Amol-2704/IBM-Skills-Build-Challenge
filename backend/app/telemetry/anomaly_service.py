from app.models.telemetry import TelemetryRecord
from app.repositories.telemetry_repo import Telemetry_repo

class AnomalyService:
    def __init__(
        self, 
        telemetry_repo: Telemetry_repo | None = None
    ):

        self.repository = telemetry_repo or Telemetry_repo() 

    def get_anomaly(
        self,
        anomaly_id: str
    ) -> TelemetryRecord:

        telemetry = self.repository.get_by_anomaly_id(
            anomaly_id
        )

        if telemetry is None:
            raise ValueError(
                f"Anomaly ;'{anomaly_id}' not found."

            )

        return telemetry
    def calculate_severity(
        self,
        telemetry: TelemetryRecord
    ) -> str: 

        if (
            telemetry.battery_temperature >= 35
            or telemetry.battery_voltage <= 27
        ): 

            return "CRITICAL"

        if (
            telemetry.battery_temperature >= 29
            or telemetry.current_draw >= 4.5
        ):

            return "HIGH"

        if (
            telemetry.battery_temperature >= 27
            or telemetry.current_draw >= 4.0
        ): 
            return "MEDIUM"

        return "LOW"

    def detect(self, context) -> list[dict]:
        anomalies = []
        if context.severity in ["CRITICAL", "HIGH"]:
            anomalies.append({
                "type": "threshold_violation",
                "description": f"High severity anomaly in {context.subsystem}"
            })
        return anomalies

anomaly_service = AnomalyService()


