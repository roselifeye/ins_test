<template>
  <div class="left-panel">
    <el-card shadow="hover" class="section">
      <template #header>
        <div class="card-header">模式与模型</div>
      </template>
      <div class="field">
        <el-radio-group v-model="modeRef" @change="store.resetResult">
          <el-radio-button label="compare">多模型对比</el-radio-button>
          <el-radio-button label="jury">AI 评审团</el-radio-button>
        </el-radio-group>
      </div>

      <div v-if="modeRef.value === 'compare'" class="field">
        <div class="section-title">选择模型（最多 3 个）</div>
        <el-checkbox-group v-model="selectedModelsRef">
          <el-checkbox
            v-for="model in modelsRef.value"
            :key="model.id"
            :label="model.id"
            :disabled="isModelDisabled(model.id)"
          >
            <div class="checkbox-content">
              <div class="name">{{ model.name }}</div>
              <div class="desc">{{ model.description }}</div>
            </div>
          </el-checkbox>
        </el-checkbox-group>
      </div>

      <div v-else class="field">
        <div class="section-title">评审角色</div>
        <div class="roles">
          <div v-for="role in juryRolesRef.value" :key="role.id" class="role-item">
            <div class="role-header">
              <el-checkbox
                :model-value="isRoleSelected(role.id)"
                @change="(checked: boolean) => handleRoleToggle(role.id, checked)"
              >
                <span class="name">{{ role.name }}</span>
                <span class="desc">{{ role.description }}</span>
              </el-checkbox>
            </div>
            <div v-if="isRoleSelected(role.id)" class="role-slider">
              <el-slider
                :model-value="getRoleWeight(role.id)"
                :min="0.5"
                :max="3"
                :step="0.5"
                show-input
                @change="(value: number) => handleRoleWeight(role.id, value)"
              />
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="hover" class="section">
      <template #header>
        <div class="card-header">检测器配置</div>
      </template>
      <div class="detector-list">
        <div v-for="detector in detectorsRef.value" :key="detector.id" class="detector-item">
          <div class="detector-header">
            <el-switch
              :model-value="selectedDetectorsRef.value[detector.id]?.enabled"
              @change="(value: boolean) => handleDetectorToggle(detector.id, value)"
            />
            <div class="meta">
              <div class="label">{{ detector.label }}</div>
              <div class="desc">{{ detector.description }}</div>
            </div>
          </div>
          <div v-if="selectedDetectorsRef.value[detector.id]?.enabled" class="detector-slider">
            <el-slider
              :model-value="selectedDetectorsRef.value[detector.id]?.threshold ?? detector.default_threshold"
              :min="0"
              :max="1"
              :step="0.05"
              show-input
              @change="(value: number) => handleDetectorThreshold(detector.id, value)"
            />
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="hover" class="section">
      <template #header>
        <div class="card-header">大模型连接</div>
      </template>
      <el-form label-position="top">
        <el-form-item label="API 地址">
          <el-input v-model="llmBaseUrlRef" placeholder="https://api.openai.com/v1" />
        </el-form-item>
        <el-form-item label="Token">
          <el-input v-model="llmApiKeyRef" placeholder="sk-..." show-password />
        </el-form-item>
      </el-form>
      <div class="tip">未填写时将使用后端默认配置并返回本地模拟结果。</div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import { useEvaluationStore } from '../store/evaluation';

const store = useEvaluationStore();
const {
  mode: modeRef,
  models: modelsRef,
  juryRoles: juryRolesRef,
  detectors: detectorsRef,
  selectedDetectors: selectedDetectorsRef,
  selectedModels: selectedModelsRef,
  selectedRoles: selectedRolesRef,
  llmBaseUrl: llmBaseUrlRef,
  llmApiKey: llmApiKeyRef
} = storeToRefs(store);

function isModelDisabled(modelId: string) {
  return (
    modeRef.value === 'compare' &&
    !selectedModelsRef.value.includes(modelId) &&
    selectedModelsRef.value.length >= 3
  );
}

function isRoleSelected(roleId: string) {
  return selectedRolesRef.value.some((role) => role.id === roleId);
}

function getRoleWeight(roleId: string) {
  return selectedRolesRef.value.find((role) => role.id === roleId)?.weight ?? 1;
}

function handleRoleToggle(roleId: string, checked: boolean) {
  const weight = getRoleWeight(roleId);
  store.updateRoles(roleId, weight, checked);
}

function handleRoleWeight(roleId: string, weight: number) {
  store.updateRoles(roleId, weight, true);
}

function handleDetectorToggle(detectorId: string, enabled: boolean) {
  store.toggleDetector(detectorId, enabled);
}

function handleDetectorThreshold(detectorId: string, threshold: number) {
  store.updateDetectorThreshold(detectorId, threshold);
}
</script>

<style scoped>
.left-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.checkbox-content .name {
  font-weight: 600;
}

.checkbox-content .desc {
  font-size: 12px;
  color: #909399;
}

.roles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.role-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 8px 12px;
}

.role-header .name {
  font-weight: 600;
  margin-right: 4px;
}

.role-header .desc {
  font-size: 12px;
  color: #909399;
  margin-left: 4px;
}

.role-slider {
  margin-top: 8px;
}

.detector-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detector-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 8px 12px;
}

.detector-header {
  display: flex;
  gap: 12px;
  align-items: center;
}

.detector-header .meta {
  flex: 1;
}

.detector-header .label {
  font-weight: 600;
}

.detector-header .desc {
  font-size: 12px;
  color: #909399;
}

.detector-slider {
  margin-top: 8px;
}

.tip {
  font-size: 12px;
  color: #909399;
}

.card-header {
  font-weight: 700;
  font-size: 16px;
}
</style>
