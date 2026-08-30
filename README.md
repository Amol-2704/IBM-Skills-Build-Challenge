## NEXUS — Mission Intelligence

NEXUS is an AI-assisted mission intelligence console for investigating spacecraft telemetry anomalies. It turns a selected anomaly into a clear operational assessment: the affected subsystem, traceable threshold signals, related historical incidents, applicable procedures, confidence, and recommended next steps.

Built for the IBM AI Builders Challenge.

## Why NEXUS

Mission operations teams must make fast, high-consequence decisions from fragmented telemetry and operational knowledge. NEXUS brings those sources together in a focused investigation workflow so an operator can move from an anomaly ID to an evidence-backed response plan in seconds.

## What it does

- Accepts a telemetry anomaly ID, such as `ANOM-001`.
- Evaluates deterministic metric thresholds for temperature, current draw, and voltage.
- Produces human-readable signals with observed values, thresholds, and severity.
- Correlates the affected subsystem with historical incidents and operational procedures.
- Handles equivalent subsystem terminology, including Power ↔ Battery.
- Calculates a deterministic, evidence-weighted confidence score.
- Returns recommended next steps based on the matching procedure and prior resolutions.
- Presents the result in a polished NEXUS Mission Intelligence dashboard.

## Architecture

```text
Next.js dashboard
        |
        | POST /investigate
        v
FastAPI investigation API
        |
        +--> Telemetry repository
        +--> Rule-based anomaly engine
        +--> Context and evidence correlation
        +--> Historical incidents and procedures
```

The current reasoning layer is deterministic by design: every signal, confidence contribution, and recommended action can be traced back to local mission data or an explicit threshold rule. This makes the demo reliable and explainable without requiring external model credentials.

## Technology

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, Pydantic, Python
- Data: local JSON telemetry, historical incident, and procedure datasets

## Quick start

### 1. Start the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts at `http://127.0.0.1:8000`. Interactive documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` and investigate `ANOM-001`.

## Demo flow

1. Enter `ANOM-001` in the dashboard.
2. Select **Investigate**.
3. Review the HIGH-severity Power anomaly.
4. Inspect the two threshold signals: elevated battery temperature and current draw.
5. Review the related Battery temperature incident and investigation procedure.
6. Explain that the confidence score is evidence-weighted, rather than hardcoded.
7. Show the recommended procedure steps and the previous incident resolution.

## Example investigation result

`ANOM-001` returns a HIGH-severity Power investigation with:

- telemetry snapshot from Orbital Operations;
- battery temperature and current-draw threshold violations;
- a matching historical battery-temperature incident;
- the Battery thermal investigation procedure;
- procedure-driven next steps and the previous resolution;
- deterministic confidence based on available telemetry, signals, historical evidence, and procedure coverage.

## API

### Investigate an anomaly

`POST /investigate`

```json
{
  "query": "ANOM-001",
  "time_range": "24h"
}
```

The response includes `severity`, `summary`, `anomalies`, `evidence`, `confidence`, and `next_steps`. Unknown anomaly IDs return HTTP 404.

## Validation

```powershell
cd frontend
npm run lint
npm run build
```

Backend API documentation and a representative investigation can be checked at `http://127.0.0.1:8000/docs` after starting the backend.

## Project structure

```text
backend/
  app/
    api/              FastAPI routes
    context/          mission context and evidence correlation
    repositories/     local telemetry access
    services/         investigation orchestration
    telemetry/        deterministic anomaly rules
  Data/               telemetry, incidents, and procedures
frontend/
  src/app/            NEXUS dashboard
  src/services/       API client and result types
```

## Future direction

NEXUS is structured so an LLM reasoning layer can be added later as an optional narrative assistant. The evidence engine and deterministic rules remain the system of record, keeping recommendations explainable and operationally dependable.
