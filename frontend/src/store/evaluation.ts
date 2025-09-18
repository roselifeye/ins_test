import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { fetchConfig, submitEvaluation } from '../api/service';
import type {
  CompareRequest,
  DetectorOption,
  DetectorSelection,
  EvaluationMode,
  EvaluationRequest,
  EvaluationResponse,
  JuryRoleOption,
  JuryRoleSelection,
  ModelOption
} from '../api/types';

export const useEvaluationStore = defineStore('evaluation', () => {
  const loading = ref(false);
  const submitting = ref(false);
  const mode = ref<EvaluationMode>('compare');
  const inputText = ref('');
  const llmBaseUrl = ref('');
  const llmApiKey = ref('');

  const models = ref<ModelOption[]>([]);
  const detectors = ref<DetectorOption[]>([]);
  const juryRoles = ref<JuryRoleOption[]>([]);

  const selectedModels = ref<string[]>([]);
  const selectedRoles = ref<JuryRoleSelection[]>([]);
  const selectedDetectors = ref<Record<string, DetectorSelection>>({});

  const result = ref<EvaluationResponse | null>(null);
  const errorMessage = ref('');

  const activeDetectors = computed(() =>
    Object.values(selectedDetectors.value).filter((item) => item.enabled)
  );

  async function initialise() {
    loading.value = true;
    try {
      const config = await fetchConfig();
      models.value = config.models;
      detectors.value = config.detectors;
      juryRoles.value = config.jury_roles;

      detectors.value.forEach((detector) => {
        selectedDetectors.value[detector.id] = {
          id: detector.id,
          enabled: true,
          threshold: detector.default_threshold
        };
      });
    } catch (error) {
      errorMessage.value = '加载配置失败，请稍后重试。';
    } finally {
      loading.value = false;
    }
  }

  function toggleDetector(detectorId: string, enabled: boolean) {
    const current = selectedDetectors.value[detectorId];
    if (current) {
      current.enabled = enabled;
    } else {
      selectedDetectors.value[detectorId] = { id: detectorId, enabled };
    }
  }

  function updateDetectorThreshold(detectorId: string, threshold: number) {
    const current = selectedDetectors.value[detectorId];
    if (current) {
      current.threshold = threshold;
    }
  }

  function updateRoles(roleId: string, weight: number, checked: boolean) {
    if (checked) {
      const existing = selectedRoles.value.find((role) => role.id === roleId);
      if (existing) {
        existing.weight = weight;
      } else {
        selectedRoles.value.push({ id: roleId, weight });
      }
    } else {
      selectedRoles.value = selectedRoles.value.filter((role) => role.id !== roleId);
    }
  }

  function resetResult() {
    result.value = null;
    errorMessage.value = '';
  }

  async function submit() {
    submitting.value = true;
    errorMessage.value = '';
    try {
      if (mode.value === 'compare' && selectedModels.value.length === 0) {
        throw new Error('请选择至少一个对比模型。');
      }
      if (mode.value === 'jury' && selectedRoles.value.length === 0) {
        throw new Error('至少选择一位评审角色。');
      }

      const payload: EvaluationRequest = {
        mode: mode.value,
        llm: {
          base_url: llmBaseUrl.value,
          api_key: llmApiKey.value
        }
      };

      const detectorsPayload = activeDetectors.value;

      if (mode.value === 'compare') {
        const comparePayload: CompareRequest = {
          input_text: inputText.value,
          models: selectedModels.value,
          detectors: detectorsPayload
        };
        payload.compare = comparePayload;
      } else {
        payload.jury = {
          input_text: inputText.value,
          roles: selectedRoles.value,
          detectors: detectorsPayload
        };
      }

      result.value = await submitEvaluation(payload);
    } catch (error: unknown) {
      errorMessage.value =
        error instanceof Error ? error.message : '请求失败，请检查网络或配置。';
    } finally {
      submitting.value = false;
    }
  }

  return {
    loading,
    submitting,
    mode,
    inputText,
    llmBaseUrl,
    llmApiKey,
    models,
    detectors,
    juryRoles,
    selectedModels,
    selectedRoles,
    selectedDetectors,
    result,
    errorMessage,
    initialise,
    toggleDetector,
    updateDetectorThreshold,
    updateRoles,
    resetResult,
    submit
  };
});
