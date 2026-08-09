from app.core.config import BASE_DIR
import json
from pathlib import Path

from app.models.telemetry import TelemetryRecord

DATA_FILE = BASE_DIR / "data" / "telemetry.json"

class Telemetry_repo:

    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file

    def get_all(self) -> list[TelemetryRecord]:
        if not self.data_file.exists():
            return[]

        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            TelemetryRecord(**record)
            for record in data
        ]

    def get_by_anomaly_id(
        self,
        anomaly_id: str
    ) -> TelemetryRecord | None:

        records = self.get_all()

        for record in records:
            if record.anomaly_id == anomaly_id:
                return record

        return None