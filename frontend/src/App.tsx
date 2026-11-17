import React, { useState, useEffect } from 'react';
import { WorkflowAnalyticsResponse } from './types';

export const App: React.FC = () => {
  const [data, setData] = useState<WorkflowAnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/workflow')
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', background: '#090d16', color: '#f8fafc', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Inter, sans-serif' }}>
        <p>Loading developer workflow intelligence...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ minHeight: '100vh', background: '#090d16', color: '#f8fafc', padding: '40px', fontFamily: 'Inter, sans-serif' }}>
        <p>Could not connect to backend at localhost:8000.</p>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: '#090d16', color: '#f8fafc', padding: '32px 24px', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <header style={{ marginBottom: '32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1e293b', paddingBottom: '20px' }}>
          <div>
            <h1 style={{ margin: '0 0 6px', fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #10b981, #06b6d4)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Developer Workflow Intelligence Platform
            </h1>
            <p style={{ margin: 0, color: '#94a3b8', fontSize: '0.92rem' }}>
              Repository: <code style={{ color: '#38bdf8' }}>{data.repo_name}</code> · Window: {data.time_window_days} days · DORA Tier: <span style={{ color: '#10b981', fontWeight: 700 }}>{data.dora.performance_tier}</span>
            </p>
          </div>
          <button style={{ background: '#0284c7', color: '#fff', border: 'none', padding: '8px 16px', borderRadius: '6px', fontWeight: 600, cursor: 'pointer' }}>
            Sync GitHub Telemetry
          </button>
        </header>

        {/* DORA Scorecard Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '24px' }}>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #10b981' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600 }}>Lead Time For Changes</span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc', margin: '8px 0 4px' }}>{data.dora.lead_time_for_changes_hours}h</div>
            <span style={{ fontSize: '0.78rem', color: '#10b981' }}>Top 15% industry benchmark</span>
          </div>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #38bdf8' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600 }}>Deployment Frequency</span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc', margin: '8px 0 4px' }}>{data.dora.deployment_frequency_per_week}/wk</div>
            <span style={{ fontSize: '0.78rem', color: '#38bdf8' }}>Multiple daily production builds</span>
          </div>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #f59e0b' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600 }}>Change Failure Rate</span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc', margin: '8px 0 4px' }}>{data.dora.change_failure_rate_percent}%</div>
            <span style={{ fontSize: '0.78rem', color: '#f59e0b' }}>Low rollback frequency</span>
          </div>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #a855f7' }}>
            <span style={{ fontSize: '0.8rem', color: '#94a3b8', textTransform: 'uppercase', fontWeight: 600 }}>Mean Time To Restore (MTTR)</span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f8fafc', margin: '8px 0 4px' }}>{data.dora.mean_time_to_restore_hours}h</div>
            <span style={{ fontSize: '0.78rem', color: '#a855f7' }}>Fast automated recovery</span>
          </div>
        </div>

        {/* Cycle Time Decomposition */}
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '24px', marginBottom: '24px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '1.15rem' }}>Average Cycle Time Phase Breakdown</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px' }}>
              <span style={{ color: '#94a3b8', fontSize: '0.82rem' }}>1. Coding Time</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#38bdf8', marginTop: '4px' }}>{data.avg_cycle_breakdown.avg_coding_hours}h</div>
              <small style={{ color: '#64748b' }}>First commit to PR open</small>
            </div>
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px' }}>
              <span style={{ color: '#94a3b8', fontSize: '0.82rem' }}>2. Pickup Latency</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f59e0b', marginTop: '4px' }}>{data.avg_cycle_breakdown.avg_pickup_hours}h</div>
              <small style={{ color: '#64748b' }}>PR open to first review</small>
            </div>
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px' }}>
              <span style={{ color: '#94a3b8', fontSize: '0.82rem' }}>3. Review Time</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#10b981', marginTop: '4px' }}>{data.avg_cycle_breakdown.avg_review_hours}h</div>
              <small style={{ color: '#64748b' }}>First review to approval</small>
            </div>
            <div style={{ background: '#0f172a', padding: '16px', borderRadius: '8px' }}>
              <span style={{ color: '#94a3b8', fontSize: '0.82rem' }}>4. Total Cycle Time</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#f8fafc', marginTop: '4px' }}>{data.avg_cycle_breakdown.avg_total_hours}h</div>
              <small style={{ color: '#64748b' }}>Total delivery lead time</small>
            </div>
          </div>
        </div>

        {/* Bottleneck Alerts */}
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '24px', marginBottom: '24px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '1.15rem' }}>Active Workflow Bottlenecks & Friction</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.active_bottlenecks.map((alert) => (
              <div key={alert.id} style={{ background: '#0f172a', border: '1px solid #334155', borderLeft: `4px solid ${alert.severity === 'critical' ? '#ef4444' : '#f59e0b'}`, padding: '16px', borderRadius: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <strong style={{ color: '#f8fafc', fontSize: '1rem' }}>PR #{alert.pr_number}: {alert.pr_title}</strong>
                  <span style={{ textTransform: 'uppercase', fontSize: '0.72rem', fontWeight: 700, padding: '3px 8px', borderRadius: '4px', background: alert.severity === 'critical' ? '#7f1d1d' : '#78350f', color: '#fff' }}>
                    {alert.severity}
                  </span>
                </div>
                <p style={{ margin: '0 0 8px', color: '#cbd5e1', fontSize: '0.9rem' }}>{alert.message}</p>
                <div style={{ fontSize: '0.82rem', color: '#10b981' }}>
                  <strong>Action:</strong> {alert.recommended_action}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Recommendations */}
        <div style={{ background: '#1e293b', borderRadius: '12px', padding: '24px' }}>
          <h3 style={{ margin: '0 0 16px', fontSize: '1.15rem' }}>AI-Generated Engineering Insights</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
            {data.ai_insights.map((insight, idx) => (
              <div key={idx} style={{ background: '#0f172a', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
                <span style={{ color: '#38bdf8', fontSize: '0.78rem', textTransform: 'uppercase', fontWeight: 700 }}>{insight.category}</span>
                <p style={{ margin: '8px 0', fontSize: '0.92rem', color: '#e2e8f0', lineHeight: 1.5 }}>{insight.summary}</p>
                <div style={{ background: 'rgba(2, 132, 199, 0.1)', border: '1px solid #0284c7', borderRadius: '6px', padding: '10px 12px', fontSize: '0.82rem', color: '#bae6fd' }}>
                  <strong>Coaching:</strong> {insight.recommendation}
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;
