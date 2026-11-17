from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class PullRequestMetrics(BaseModel):
    id: str
    number: int
    title: str
    author: str
    status: str  # open, merged, closed
    lines_added: int
    lines_deleted: int
    files_changed: int
    created_at: datetime
    merged_at: Optional[datetime] = None
    coding_hours: float = Field(..., description="Hours from first commit to PR open")
    pickup_hours: float = Field(..., description="Hours from PR open to first review")
    review_hours: float = Field(..., description="Hours from first review to merge")
    total_cycle_hours: float = Field(..., description="Total lead time")

class BottleneckAlert(BaseModel):
    id: str
    pr_number: int
    pr_title: str
    severity: str  # low, medium, high, critical
    category: str  # review_stalling, large_diff, stale_unassigned
    message: str
    waiting_hours: float
    recommended_action: str

class DoraSummary(BaseModel):
    lead_time_for_changes_hours: float
    deployment_frequency_per_week: float
    change_failure_rate_percent: float
    mean_time_to_restore_hours: float
    performance_tier: str  # Elite, High, Medium, Low

class AIInsight(BaseModel):
    category: str
    summary: str
    impact_level: str
    recommendation: str

class WorkflowAnalyticsResponse(BaseModel):
    repo_name: str
    time_window_days: int
    dora: DoraSummary
    avg_cycle_breakdown: dict
    active_bottlenecks: List[BottleneckAlert]
    recent_prs: List[PullRequestMetrics]
    ai_insights: List[AIInsight]
