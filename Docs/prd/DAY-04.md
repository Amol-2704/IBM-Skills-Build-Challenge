---

# NEXUS
## Daily PRD

**Sprint:** Sprint 1 — Foundation & Context Engine  
**Day:** 04  
**Date:** August 2026  
**Status:** Ready for Development

---

# Theme

**Building the Mission Intelligence Foundation**

Today is about creating the **Context Engine**, the component that transforms raw telemetry into meaningful mission context. This is the first feature that differentiates NEXUS from a traditional monitoring dashboard.

---

# Sprint Goal

Deliver the first end-to-end investigation workflow:

```text
Mission Dashboard
        ↓
Telemetry
        ↓
Anomaly
        ↓
Context Engine
        ↓
Investigation Panel
```

---

# Problem Statement

Mission operators receive telemetry and alerts, but the information needed to understand an anomaly is distributed across procedures, historical incidents, mission metadata, and recent events.

The challenge is not detecting an anomaly—it is gathering the right context quickly enough to support a good decision.

Today's work begins solving that problem.

---

# Objectives

By the end of today, NEXUS should be able to:

- detect a simulated anomaly
- build a structured investigation context
- expose it through the backend API
- display it inside the frontend investigation panel

No AI reasoning yet.

---

# User Story

**As a mission operator**

When an anomaly occurs,

I want to see every relevant piece of operational context in one place,

so I can understand the situation before deciding what to do.

---

# Deliverables

## Backend

### Context Service

Create

```text
backend/app/context/context_service.py
```

Responsibilities

- Load mission information
- Load telemetry
- Load recent events
- Load historical incidents
- Load procedures
- Combine them into one investigation object

---

### Investigation Model

Create

```text
backend/app/schemas/investigation.py
```

Example

```python
InvestigationContext
```

containing

- anomaly
- subsystem
- severity
- mission phase
- telemetry
- historical incidents
- procedures
- recent events
- generated timestamp

---

### API

Implement

```http
POST /api/investigate
```

Input

```json
{
  "anomalyId": "ANOM-001"
}
```

Output

```json
{
  "context": {}
}
```

---

## Data

Create sample repositories

```text
data/
```

```
historical/

procedures/

events/
```

Populate each with realistic JSON data.

---

## Frontend

Create

```text
InvestigationPanel
```

Display

```
Mission Phase

Affected Subsystem

Severity

Telemetry Snapshot

Historical Incidents

Procedures

Recent Events
```

The frontend should request data from the backend rather than hardcoding it.

---

# Non-Goals

Today we are **not** implementing:

- LLM integration
- Vector search
- AI reasoning
- Recommendations
- Risk scoring
- Database persistence
- Authentication

---

# Acceptance Criteria

- Context Service implemented
- Investigation API operational
- Historical data loaded
- Procedures loaded
- Investigation Panel displays backend data
- No hardcoded context inside the UI

---

# Definition of Done

A mission operator can click **Investigate** and receive a structured investigation context generated from multiple data sources.

---

# Architecture

```text
Telemetry
      │
      ▼
Anomaly Detection
      │
      ▼
Context Service
      │
 ┌────┼────┐
 ▼    ▼    ▼
Events Procedures History
      │
      ▼
Investigation Context
      │
      ▼
Frontend
```

---

# Engineering Tasks

| Priority | Task | Status |
|----------|------|--------|
| 🔴 High | Build Context Service | ⬜ |
| 🔴 High | Create Investigation Schema | ⬜ |
| 🔴 High | Implement `/api/investigate` | ⬜ |
| 🟠 Medium | Add historical incidents JSON | ⬜ |
| 🟠 Medium | Add procedures JSON | ⬜ |
| 🟠 Medium | Build Investigation Panel | ⬜ |
| 🟢 Low | Improve UI styling | ⬜ |

---

# Git Milestones

```bash
feat: create investigation context schema

feat: implement context aggregation service

feat: add investigate API endpoint

feat: build investigation panel UI
```

---

# Risks

- Avoid tightly coupling the frontend to the backend response format.
- Keep the Context Engine deterministic; AI reasoning will be added later.
- Use realistic but simulated mission data.

---

# End-of-Day Deliverable

The demo should follow this flow:

```text
Mission Dashboard
        │
        ▼
⚠ Battery Temperature Anomaly
        │
        ▼
Click "Investigate"
        │
        ▼
Backend aggregates:
• Telemetry
• Mission Phase
• Procedures
• Historical Incidents
• Recent Events
        │
        ▼
Frontend displays the complete Investigation Context
```

---

## New workflow (starting today)

From now until the IBM AI Builders Challenge submission, every day will follow the same structure:

1. 📄 **Daily PRD** (scope and success criteria)
2. 🏗️ **Architecture discussion** (if needed)
3. 💻 **Implementation**
4. 🧪 **Testing**
5. 📝 **Daily Decision Log (ADR if applicable)**
6. ✅ **Git commits**
7. 📅 **Plan for the next day**

This keeps us focused and gives us a professional development trail that we can also reference in the final presentation.