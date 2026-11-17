"""
Bottleneck Detector for engineering workflows.
Detects review queue stalling, oversized review batches, and stale pull requests.
"""

from typing import List
from app.models.schemas import PullRequestMetrics, BottleneckAlert

class BottleneckDetector:
    def detect(self, prs: List[PullRequestMetrics]) -> List[BottleneckAlert]:
        alerts: List[BottleneckAlert] = []

        for pr in prs:
            if pr.status != "open":
                continue

            # 1. Extreme Pickup Delay (>36 hours)
            if pr.pickup_hours > 36.0:
                severity = "critical" if pr.pickup_hours > 48.0 else "high"
                alerts.append(BottleneckAlert(
                    id=f"alert-pickup-{pr.number}",
                    pr_number=pr.number,
                    pr_title=pr.title,
                    severity=severity,
                    category="review_stalling",
                    message=f"PR #{pr.number} has been waiting {pr.pickup_hours:.1f} hours for an initial review.",
                    waiting_hours=round(pr.pickup_hours, 1),
                    recommended_action="Notify assigned squad reviewers via Slack/Teams or reassign during daily standup."
                ))

            # 2. Oversized Diff Inertia (>500 LOC changed)
            total_loc = pr.lines_added + pr.lines_deleted
            if total_loc > 500:
                alerts.append(BottleneckAlert(
                    id=f"alert-loc-{pr.number}",
                    pr_number=pr.number,
                    pr_title=pr.title,
                    severity="high" if total_loc > 1000 else "medium",
                    category="large_diff",
                    message=f"Large change size ({total_loc} lines across {pr.files_changed} files) causes high review inertia.",
                    waiting_hours=round(pr.total_cycle_hours, 1),
                    recommended_action="Split into stacked atomic PRs (e.g. database schema change first, followed by business logic)."
                ))

        return alerts
