import { apiClient } from './client';
import type {
  EvaluationConfigResponse,
  EvaluationRequest,
  EvaluationResponse
} from './types';

export async function fetchConfig() {
  const { data } = await apiClient.get<EvaluationConfigResponse>('/evaluation/config');
  return data;
}

export async function submitEvaluation(payload: EvaluationRequest) {
  const { data } = await apiClient.post<EvaluationResponse>('/evaluation/evaluate', payload);
  return data;
}
