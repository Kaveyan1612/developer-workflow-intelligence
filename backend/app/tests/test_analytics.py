"""
Tests for Developer Workflow Intelligence Platform.
"""

from app.services.analytics_engine import AnalyticsEngine
from app.services.bottleneck_detector import BottleneckDetector
from app.services.ai_insights import AIInsightsGenerator

def test_analytics_dora_computation():
    engine = AnalyticsEngine()
    dora = engine.compute_dora_metrics()
    assert dora.lead_time_for_changes_hours > 0
    assert dora.deployment_frequency_per_week > 0
    assert dora.performance_tier in ["Elite", "High", "Medium", "Low"]

def test_cycle_time_breakdown():
    engine = AnalyticsEngine()
    breakdown = engine.compute_cycle_breakdown()
    assert "avg_coding_hours" in breakdown
    assert "avg_pickup_hours" in breakdown
    assert "avg_review_hours" in breakdown
    assert breakdown["avg_total_hours"] >= breakdown["avg_coding_hours"]

def test_bottleneck_detection():
    engine = AnalyticsEngine()
    detector = BottleneckDetector()
    prs = engine.get_recent_prs()
    bottlenecks = detector.detect(prs)
    assert len(bottlenecks) > 0
    # Should detect PR #104 with 52h pickup delay and 1240+ lines
    p104_alerts = [b for b in bottlenecks if b.pr_number == 104]
    assert len(p104_alerts) >= 1

def test_ai_insights_generation():
    engine = AnalyticsEngine()
    detector = BottleneckDetector()
    ai_gen = AIInsightsGenerator()

    prs = engine.get_recent_prs()
    dora = engine.compute_dora_metrics()
    breakdown = engine.compute_cycle_breakdown()
    insights = ai_gen.generate(prs, dora, breakdown)

    assert len(insights) >= 2
    categories = [i.category for i in insights]
    assert any("Review" in c for c in categories)
