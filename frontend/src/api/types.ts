export interface ModelOption {
  id: string;
  name: string;
  description?: string;
}

export interface DetectorOption {
  id: string;
  label: string;
  description?: string;
  default_threshold: number;
}

export interface JuryRoleOption {
  id: string;
  name: string;
  description: string;
}

export interface EvaluationConfigResponse {
  models: ModelOption[];
  detectors: DetectorOption[];
  jury_roles: JuryRoleOption[];
}

export type EvaluationMode = 'compare' | 'jury';

export interface DetectorSelection {
  id: string;
  enabled: boolean;
  threshold?: number;
}

export interface CompareRequest {
  input_text: string;
  models: string[];
  detectors: DetectorSelection[];
}

export interface JuryRoleSelection {
  id: string;
  weight: number;
}

export interface JuryRequest {
  input_text: string;
  roles: JuryRoleSelection[];
  detectors: DetectorSelection[];
}

export interface LLMConfig {
  base_url: string;
  api_key: string;
}

export interface EvaluationRequest {
  mode: EvaluationMode;
  compare?: CompareRequest;
  jury?: JuryRequest;
  llm?: Partial<LLMConfig>;
}

export interface DiffSnippet {
  model_id: string;
  content: string;
  highlighted_diff: string[];
}

export interface DetectorIssue {
  detector_id: string;
  severity: string;
  summary: string;
  evidence: string;
}

export interface CompareResult {
  generated_at: string;
  completions: Record<string, string>;
  diffs: DiffSnippet[];
  detector_issues: DetectorIssue[];
}

export interface JuryRoleOpinion {
  role_id: string;
  summary: string;
  score: number;
  recommendations: string[];
}

export interface JuryAggregate {
  overall_score: number;
  radar: Record<string, number>;
  consensus: Record<string, number>;
}

export interface JuryResult {
  generated_at: string;
  opinions: JuryRoleOpinion[];
  aggregate: JuryAggregate;
  detector_issues: DetectorIssue[];
}

export interface EvaluationResponse {
  mode: EvaluationMode;
  compare_result?: CompareResult;
  jury_result?: JuryResult;
}
