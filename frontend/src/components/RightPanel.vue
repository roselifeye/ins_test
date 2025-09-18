<template>
  <div class="right-panel">
    <el-card shadow="hover" class="section">
      <template #header>
        <div class="card-header">待评估内容</div>
      </template>
      <el-input
        v-model="inputTextRef"
        type="textarea"
        :rows="12"
        placeholder="粘贴需要评估的文本，或根据 PRD 提供业务需求描述"
        @input="store.resetResult"
      />
      <div class="action-bar">
        <el-button type="primary" :loading="submittingRef" @click="handleSubmit" round>
          运行评估
        </el-button>
        <el-button @click="store.resetResult" round>清除结果</el-button>
        <el-alert
          v-if="store.errorMessage"
          :title="store.errorMessage"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
    </el-card>

    <el-card v-if="store.result" shadow="hover" class="section">
      <template #header>
        <div class="card-header">评估结果</div>
      </template>
      <div v-if="store.result.mode === 'compare' && store.result.compare_result">
        <compare-result :result="store.result.compare_result" />
      </div>
      <div v-else-if="store.result.mode === 'jury' && store.result.jury_result">
        <jury-result :result="store.result.jury_result" />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import CompareResult from './results/CompareResult.vue';
import JuryResult from './results/JuryResult.vue';
import { useEvaluationStore } from '../store/evaluation';

const store = useEvaluationStore();
const { inputText: inputTextRef, submitting: submittingRef } = storeToRefs(store);

async function handleSubmit() {
  if (!inputTextRef.value.trim()) {
    store.errorMessage = '请输入需要评估的文本。';
    return;
  }
  await store.submit();
}
</script>

<style scoped>
.right-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section {
  width: 100%;
}

.action-bar {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
}

.action-bar .el-alert {
  flex: 1;
}

.card-header {
  font-weight: 700;
  font-size: 16px;
}
</style>
