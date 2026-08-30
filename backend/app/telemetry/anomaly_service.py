from app.models.telemetry import TelemetryRecord
from app.repositories.telemetry_repo import Telemetry_repo

class AnomalyService:
    """Rule-based telemetry analysis with explanations suitable for operators."""
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
        """Return one traceable signal for each breached operating threshold."""
        telemetry = context.telemetry
        signals: list[dict] = []
        rules = (
            ("battery_temperature", 35.0, ">=", "critical", "Battery temperature is at or above the critical 35.0°C limit."),
            ("battery_temperature", 29.0, ">=", "high", "Battery temperature is above the 29.0°C high-risk threshold."),
            ("battery_temperature", 27.0, ">=", "medium", "Battery temperature is above the 27.0°C watch threshold."),
            ("current_draw", 4.5, ">=", "high", "Current draw is above the 4.5 A high-risk threshold."),
            ("current_draw", 4.0, ">=", "medium", "Current draw is above the 4.0 A watch threshold."),
            ("battery_voltage", 27.0, "<=", "critical", "Battery voltage is at or below the critical 27.0 V limit."),
        )

        severity_rank = {"critical": 3, "high": 2, "medium": 1}
        for metric, threshold, operator, level, description in rules:
            value = float(telemetry[metric])
            breached = value >= threshold if operator == ">=" else value <= threshold
            if breached:
                signals.append({
                    "type": "threshold_violation",
                    "metric": metric,
                    "observed": value,
                    "operator": operator,
                    "threshold": threshold,
                    "severity": level.upper(),
                    "description": description,
                })

        # Retain only the most severe threshold for a metric; lower thresholds are
        # supporting context, not independent faults.
        strongest: dict[str, dict] = {}
        for signal in signals:
            metric = signal["metric"]
            if metric not in strongest or severity_rank[signal["severity"].lower()] > severity_rank[strongest[metric]["severity"].lower()]:
                strongest[metric] = signal
        return list(strongest.values())

anomaly_service = AnomalyService()


