# Developer Workflow Intelligence Platform

> An engineering intelligence and analytics platform that ingests repository activity (pull requests, code reviews, commits, issue lifecycles) to identify engineering bottlenecks, compute cycle times, and deliver automated workflow optimization recommendations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB.svg?logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2F%20SQLAlchemy-336791.svg?logo=postgresql)](https://www.postgresql.org)
[![DORA Metrics](https://img.shields.io/badge/Metrics-DORA%20%26%20SPACE-blueviolet.svg)](#dora-metrics-engine)

---

## Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │    React 18 + TypeScript Frontend      │
                      │  (DORA KPIs, Cycle Time Heatmaps, AI)  │
                      └───────────────────▲────────────────────┘
                                          │ REST API
                      ┌───────────────────▼────────────────────┐
                      │            FastAPI Gateway             │
                      │   - Rate-Limited Ingestion Engine      │
                      │   - Analytical Aggregation Service     │
                      └───────────▲────────────────▲───────────┘
                                  │                │
             ┌────────────────────┴───┐        ┌───┴────────────────────┐
             │                        │        │                        │
┌────────────▼──────────────┐  ┌──────▼────────▼────────┐  ┌────────────▼──────────────┐
│    GitHub API Client      │  │ PostgreSQL Persistence │  │   Workflow AI Engine      │
│  - PRs & Commits Poller   │  │  - PRs, Commits, Reviws│  │ - Bottleneck Detection    │
│  - Review Thread Parser   │  │  - Cycle Time Snapshots│  │ - Review Latency Predictor│
│  - Rate-limit aware ETL   │  │  - Developer Profiles  │  │ - Velocity Summarizer     │
└───────────────────────────┘  └────────────────────────┘  └───────────────────────────┘
```

The platform transforms raw developer git telemetry into actionable team health indicators:
1. **GitHub Ingestion Pipeline**: Ingests Pull Requests, comments, commits, CI run durations, and review submission timestamps.
2. **Cycle Time Decomposition Engine**: Segregates full lifecycle latency into 4 distinct phases:
   - **Coding Time**: First commit to PR creation.
   - **Pickup Latency**: PR creation to first substantive code review.
   - **Review Time**: First review to final PR approval.
   - **Merge & Deploy Latency**: Approval to merge and deploy timestamp.
3. **Bottleneck & Anomaly Detection**: Automatically flags PRs with extreme review latency (>48h), review debt (large diffs >500 LOC causing review inertia), and unassigned stale branches.
4. **AI-Generated Workflow Insights**: Synthesizes engineering trends, sprint velocity patterns, and provides actionable recommendations to unblock squads.

---

## Key Metrics & Capabilities

- **DORA Metrics Suite**: Lead Time for Changes, Deployment Frequency, Change Failure Rate, Time to Restore Service.
- **Review Latency Heatmap**: Highlights days and squad segments where review queues stagnate.
- **Diff Complexity Scoring**: Identifies pull requests prone to regressions based on file touch counts and modification entropy.
- **Automated Squad Coaching**: Actionable automated alerts (e.g. *"PR #142 has been waiting 3.2 days for second review; ping team lead or break down 840 LOC diff"*).

---

## Directory Structure

```
developer-workflow-intelligence/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── schemas.py           # Pydantic v2 schemas
│   │   │   └── database.py          # SQLAlchemy models & schema definitions
│   │   ├── services/
│   │   │   ├── analytics_engine.py  # Cycle time & DORA metric computations
│   │   │   ├── bottleneck_detector.py # Queue stalling & review debt rules
│   │   │   └── ai_insights.py       # Workflow summarizer & coaching generator
│   │   ├── routers/
│   │   │   └── analytics.py         # Endpoints for metrics, PRs, bottlenecks
│   │   ├── main.py                  # FastAPI application entrypoint
│   │   └── tests/
│   │       └── test_analytics.py    # Unit & metric calculation tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DoraScorecard.tsx    # Lead time, deployment frequency KPIs
│   │   │   ├── BottleneckList.tsx   # Critical review stall alerts
│   │   │   └── CycleTimeChart.tsx   # Visual phase decomposition breakdown
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── index.html
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### 1. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## Author

**Kaveyan K**  
- Email: [kaveyank1@gmail.com](mailto:kaveyank1@gmail.com)
- Portfolio: [https://kaveyan-portfolio.netlify.app/](https://kaveyan-portfolio.netlify.app/)
- GitHub: [https://github.com/Kaveyan1612](https://github.com/Kaveyan1612)
- LinkedIn: [https://linkedin.com](https://linkedin.com)
