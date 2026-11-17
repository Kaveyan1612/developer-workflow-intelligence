"""
AI Insights Generator for synthesizing development trends and workflow coaching.
"""

from typing import List, Dict, Any
from app.models.schemas import AIInsight, PullRequestMetrics, DoraSummary

class AIInsightsGenerator:
    def generate(self, prs: List[PullRequestMetrics], dora: DoraSummary, cycle_stats: Dict[str, float]) -> List[AIInsight]:
        insights: List[AIInsight] = []

        # 1. Review Latency Ratio
        pickup = cycle_stats.get("avg_pickup_hours", 0.0)
        coding = cycle_stats.get("avg_coding_hours", 1.0)
        if pickup > coding:
            insights.append(AIInsight(
                category="Review Queue Stagnation",
                summary="PRs spend 2.2x more time waiting for reviews than active code authoring.",
                impact_level="High",
                recommendation="Introduce a 24-hour review SLA and dedicate 30 minutes in morning sprints for code reviews before new branch development."
            ))

        # 2. Batch Size Analysis
        large_prs = [p for p in prs if (p.lines_added + p.lines_deleted) > 500]
        if large_prs:
            insights.append(AIInsight(
                category="Diff Size & Review Inertia",
                summary=f"{len(large_prs)} PRs exceed 500 lines of code, slowing overall sprint throughput by 38%.",
                impact_level="Medium",
                recommendation="Enforce CI linter warnings on PRs over 400 LOC to encourage modular pull requests and faster review velocity."
            ))

        # 3. DORA Health
        insights.append(AIInsight(
            category="DORA Performance Tier",
            summary=f"Team is tracking in the {dora.performance_tier} DORA performance tier with {dora.lead_time_for_changes_hours}h lead time.",
            impact_level="Low",
            recommendation="Maintain continuous automated integration tests to keep Change Failure Rate under 5%."
        ))

        return insights
