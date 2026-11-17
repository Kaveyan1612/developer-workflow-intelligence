"""
FastAPI Router for Developer Workflow Intelligence Platform.
"""

from fastapi import APIRouter
from app.models.schemas import WorkflowAnalyticsResponse
from app.services.analytics_engine import AnalyticsEngine
from app.services.bottleneck_detector import BottleneckDetector
from app.services.ai_insights import AIInsightsGenerator

router = APIRouter(prefix="/api/v1", tags=["Analytics"])

engine = AnalyticsEngine()
detector = BottleneckDetector()
ai_generator = AIInsightsGenerator()

@router.get("/workflow", response_model=WorkflowAnalyticsResponse)
async def get_workflow_analytics(repo: str = "main-platform", days: int = 14):
    """
    Returns aggregated DORA metrics, cycle time breakdown, active bottlenecks,
    and AI-generated workflow recommendations.
    """
    prs = engine.get_recent_prs()
    dora = engine.compute_dora_metrics()
    cycle_breakdown = engine.compute_cycle_breakdown()
    bottlenecks = detector.detect(prs)
    insights = ai_generator.generate(prs, dora, cycle_breakdown)

    return WorkflowAnalyticsResponse(
        repo_name=repo,
        time_window_days=days,
        dora=dora,
        avg_cycle_breakdown=cycle_breakdown,
        active_bottlenecks=bottlenecks,
        recent_prs=prs,
        ai_insights=insights
    )
