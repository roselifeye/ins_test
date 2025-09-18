<template>
  <div class="compare-result">
    <el-descriptions :column="3" border>
      <el-descriptions-item v-for="(text, modelId) in result.completions" :key="modelId" :label="modelId">
        <div class="completion">{{ text }}</div>
      </el-descriptions-item>
    </el-descriptions>

    <div class="diff-section" v-if="result.diffs.length">
      <div class="section-title">差异对比</div>
      <el-collapse>
        <el-collapse-item v-for="diff in result.diffs" :key="diff.model_id" :title="`与 ${diff.model_id} 差异`">
          <pre class="diff-block">{{ diff.highlighted_diff.join('\n') || '无明显差异' }}</pre>
        </el-collapse-item>
      </el-collapse>
    </div>

    <detector-issues :issues="result.detector_issues" />
  </div>
</template>

<script lang="ts" setup>
import DetectorIssues from './DetectorIssues.vue';
import type { CompareResult } from '../../api/types';

defineProps<{ result: CompareResult }>();
</script>

<style scoped>
.compare-result {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.completion {
  white-space: pre-wrap;
}

.diff-block {
  background-color: #1f1f1f;
  color: #f2f2f2;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}

.section-title {
  font-weight: 600;
  margin-bottom: 8px;
}
</style>
