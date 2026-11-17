"""
Analytics Engine for computing DORA metrics and granular Cycle Time breakdowns.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from app.models.schemas import PullRequestMetrics, DoraSummary

class AnalyticsEngine:
    def __init__(self):
        # High quality realistic seed data simulating an engineering repository
        now = datetime.now(timezone.utc)
        self.sample_prs: List[PullRequestMetrics] = [
            PullRequestMetrics(
                id="pr-101",
                number=101,
                title="feat(auth): Add OAuth2 PKCE flow for mobile clients",
                author="alex.dev",
                status="merged",
                lines_added=420,
                lines_deleted=45,
                files_changed=8,
                created_at=now - timedelta(days=2, hours=4),
                merged_at=now - timedelta(days=1),
                coding_hours=6.5,
                pickup_hours=14.2,
                review_hours=7.3,
                total_cycle_hours=28.0
            ),
            PullRequestMetrics(
                id="pr-102",
                number=102,
                title="refactor(database): Migrate connection pool to asyncpg",
                author="sarah.m",
                status="merged",
                lines_added=180,
                lines_deleted=110,
                files_changed=5,
                created_at=now - timedelta(days=4),
                merged_at=now - timedelta(days=3, hours=6),
                coding_hours=4.0,
                pickup_hours=5.5,
                review_hours=8.5,
                total_cycle_hours=18.0
            ),
            PullRequestMetrics(
                id="pr-103",
                number=103,
                title="fix(telemetry): Resolve memory leak in WebSocket connection buffer",
                author="kaveyan.k",
                status="merged",
                lines_added=95,
                lines_deleted=30,
                files_changed=3,
                created_at=now - timedelta(days=5),
                merged_at=now - timedelta(days=4, hours=18),
                coding_hours=3.2,
                pickup_hours=2.1,
                review_hours=3.7,
                total_cycle_hours=9.0
            ),
            PullRequestMetrics(
                id="pr-104",
                number=104,
                title="feat(billing): Stripe webhooks reconciliation worker",
                author="david.p",
                status="open",
                lines_added=1240,
                lines_deleted=80,
                files_changed=24,
                created_at=now - timedelta(days=3, hours=12),
                merged_at=None,
                coding_hours=18.0,
                pickup_hours=52.0,  # Critical stalling
                review_hours=32.0,
                total_cycle_hours=102.0
            ),
            PullRequestMetrics(
                id="pr-105",
                number=105,
                title="chore(deps): Bump dependencies and fix vulnerability advisories",
                author="renovate-bot",
                status="open",
                lines_added=65,
                lines_deleted=42,
                files_changed=2,
                created_at=now - timedelta(days=6),
                merged_at=None,
                coding_hours=0.5,
                pickup_hours=74.0,  # Stale
                review_hours=0.0,
                total_cycle_hours=74.5
            )
        ]

    def get_recent_prs(self) -> List[PullRequestMetrics]:
        return self.sample_prs

    def compute_dora_metrics(self) -> DoraSummary:
        merged = [p for p in self.sample_prs if p.status == "merged"]
        avg_lead_time = sum(p.total_cycle_hours for p in merged) / max(len(merged), 1)

        # Deployments per week estimate (3 merged PRs over 5 days ~ 4.2 per week)
        deployments_per_week = round((len(merged) / 5.0) * 7.0, 1)

        tier = "High" if avg_lead_time < 36.0 else "Medium"

        return DoraSummary(
            lead_time_for_changes_hours=round(avg_lead_time, 1),
            deployment_frequency_per_week=deployments_per_week,
            change_failure_rate_percent=3.8,
            mean_time_to_restore_hours=1.2,
            performance_tier=tier
        )

    def compute_cycle_breakdown(self) -> Dict[str, float]:
        merged = [p for p in self.sample_prs if p.status == "merged"]
        if not merged:
            return {"coding_hours": 0.0, "pickup_hours": 0.0, "review_hours": 0.0}

        return {
            "avg_coding_hours": round(sum(p.coding_hours for p in merged) / len(merged), 1),
            "avg_pickup_hours": round(sum(p.pickup_hours for p in merged) / len(merged), 1),
            "avg_review_hours": round(sum(p.review_hours for p in merged) / len(merged), 1),
            "avg_total_hours": round(sum(p.total_cycle_hours for p in merged) / len(merged), 1)
        }
