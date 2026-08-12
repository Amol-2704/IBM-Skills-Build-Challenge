import uuid

from app.context.context_service import context_service
from app.telemetry.anomaly_service import anomaly_service


class InvestigationService:

    def investigate(
        self,
        query: str,
        time_range: str = "24h"
    ):

        investigation_id = str(uuid.uuid4())

        telemetry = anomaly_service.get_anomaly(query)

        severity = anomaly_service.calculate_severity(
            telemetry
        )

        context = context_service.build_context(
            anomaly_id=query,
            telemetry=telemetry,
            severity=severity
        )

        anomalies = anomaly_service.detect(context)

        evidence = self._build_evidence(context)

        confidence = self._calculate_confidence(
            context,
            anomalies
        )

        return {
            "investigation_id": investigation_id,
            "query": query,
            "summary": self._build_summary(
                context,
                anomalies
            ),
            "anomalies": anomalies,
            "evidence": evidence,
            "confidence": confidence,
            "next_steps": self._build_next_steps(
                context,
                anomalies
            )
        }

    def _build_summary(
        self,
        context,
        anomalies
    ):

        if not anomalies:
            return [
                f"No significant anomaly detected in "
                f"{context.subsystem}."
            ]

        summary = [
            (
                f"{context.severity} severity anomaly "
                f"detected in {context.subsystem}."
            )
        ]

        # Look for similar historical incidents
        matching_incidents = [
            incident
            for incident in context.historical_incidents
            if incident.subsystem.lower()
            == context.subsystem.lower()
        ]

        if matching_incidents:
            summary.append(
                f"{len(matching_incidents)} similar "
                f"historical incident(s) found."
            )

            summary.append(
                f"Previous incident: "
                f"{matching_incidents[0].title}."
            )

        return summary

    def _build_evidence(self, context):

        evidence = []

        # Current telemetry
        evidence.append({
            "type": "telemetry",
            "data": context.telemetry
        })

        # Matching historical incidents
        matching_incidents = [
            incident
            for incident in context.historical_incidents
            if incident.subsystem.lower()
            == context.subsystem.lower()
        ]

        for incident in matching_incidents:
            evidence.append({
                "type": "historical_incident",
                "id": incident.id,
                "title": incident.title,
                "description": incident.description,
                "severity": incident.severity,
                "resolution": incident.resolution
            })

        # Matching procedures
        matching_procedures = [
            procedure
            for procedure in context.procedures
            if procedure.subsystem.lower()
            == context.subsystem.lower()
        ]

        for procedure in matching_procedures:
            evidence.append({
                "type": "procedure",
                "id": procedure.id,
                "title": procedure.title,
                "steps": procedure.steps
            })

        return evidence

    def _calculate_confidence(
        self,
        context,
        anomalies
    ):

        confidence = 0.5

        if anomalies:
            confidence += 0.2

        if context.historical_incidents:
            confidence += 0.15

        if context.procedures:
            confidence += 0.15

        return min(confidence, 1.0)

    def _build_next_steps(
        self,
        context,
        anomalies
    ):

        if not anomalies:
            return [
                "Continue monitoring the system."
            ]

        steps = []

        # Find procedures for this subsystem
        matching_procedures = [
            procedure
            for procedure in context.procedures
            if procedure.subsystem.lower()
            == context.subsystem.lower()
        ]

        # Use actual procedure steps
        for procedure in matching_procedures:
            steps.extend(procedure.steps)

        # Use historical resolution
        matching_incidents = [
            incident
            for incident in context.historical_incidents
            if incident.subsystem.lower()
            == context.subsystem.lower()
        ]

        for incident in matching_incidents:
            if incident.resolution:
                steps.append(
                    f"Previous resolution: "
                    f"{incident.resolution}"
                )

        if not steps:
            steps = [
                f"Inspect the {context.subsystem} subsystem.",
                "Review affected telemetry metrics.",
                "Continue monitoring the system."
            ]

        return steps


investigation_service = InvestigationService()