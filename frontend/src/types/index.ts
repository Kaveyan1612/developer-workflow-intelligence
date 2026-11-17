export interface PullRequestMetrics {
  id: string;
  number: number;
  title: string;
  author: string;
  status: 'open' | 'merged' | 'closed';
  lines_added: number;
  lines_deleted: number;
  files_changed: number;
  created_at: string;
  merged_at?: string;
  coding_hours: number;
  pickup_hours: number;
  review_hours: number;
  total_cycle_hours: number;
}

export interface BottleneckAlert {
  id: string;
  pr_number: number;
  pr_title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  message: string;
  waiting_hours: number;
  recommended_action: string;
}

export interface DoraSummary {
  lead_time_for_changes_hours: number;
  deployment_frequency_per_week: number;
  change_failure_rate_percent: number;
  mean_time_to_restore_hours: number;
  performance_tier: string;
}

export interface AIInsight {
  category: string;
  summary: string;
  impact_level: string;
  recommendation: string;
}

export interface WorkflowAnalyticsResponse {
  repo_name: string;
  time_window_days: number;
  dora: DoraSummary;
  avg_cycle_breakdown: {
    avg_coding_hours: number;
    avg_pickup_hours: number;
    avg_review_hours: number;
    avg_total_hours: number;
  };
  active_bottlenecks: BottleneckAlert[];
  recent_prs: PullRequestMetrics[];
  ai_insights: AIInsight[];
}
