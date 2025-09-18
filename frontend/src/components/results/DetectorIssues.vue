<template>
  <div class="detector-issues" v-if="issues.length">
    <div class="section-title">检测器发现</div>
    <el-timeline>
      <el-timeline-item
        v-for="issue in issues"
        :key="issue.detector_id + issue.summary"
        :timestamp="issue.detector_id"
        type="warning"
      >
        <div class="issue-summary">{{ issue.summary }}（严重度：{{ issue.severity }}）</div>
        <div class="issue-evidence">{{ issue.evidence }}</div>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script lang="ts" setup>
import type { DetectorIssue } from '../../api/types';

defineProps<{ issues: DetectorIssue[] }>();
</script>

<style scoped>
.section-title {
  font-weight: 600;
  margin-bottom: 8px;
}

.issue-summary {
  font-weight: 600;
}

.issue-evidence {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  white-space: pre-wrap;
}
</style>
