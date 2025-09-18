<template>
  <div class="jury-result">
    <el-card class="summary-card">
      <div class="headline">总体得分：{{ result.aggregate.overall_score.toFixed(1) }}</div>
      <div class="consensus">
        <el-tag type="success">共识度：{{ (result.aggregate.consensus.agreement * 100).toFixed(0) }}%</el-tag>
        <el-tag type="danger">少数意见：{{ (result.aggregate.consensus.dissent * 100).toFixed(0) }}%</el-tag>
      </div>
      <div class="radar">
        <el-descriptions :column="2" border>
          <el-descriptions-item
            v-for="(score, dimension) in result.aggregate.radar"
            :key="dimension"
            :label="dimension"
          >
            {{ score.toFixed(1) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>

    <el-collapse>
      <el-collapse-item
        v-for="opinion in result.opinions"
        :key="opinion.role_id"
        :title="`${opinion.role_id}（得分 ${opinion.score.toFixed(1)}）`"
      >
        <div class="opinion-summary">{{ opinion.summary }}</div>
        <div class="recommendations">
          <div v-for="recommendation in opinion.recommendations" :key="recommendation" class="recommendation">
            {{ recommendation }}
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>

    <detector-issues :issues="result.detector_issues" />
  </div>
</template>

<script lang="ts" setup>
import DetectorIssues from './DetectorIssues.vue';
import type { JuryResult } from '../../api/types';

defineProps<{ result: JuryResult }>();
</script>

<style scoped>
.jury-result {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.headline {
  font-size: 20px;
  font-weight: 700;
}

.consensus {
  display: flex;
  gap: 8px;
}

.opinion-summary {
  font-weight: 600;
  margin-bottom: 8px;
}

.recommendation {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 8px;
  white-space: pre-wrap;
}
</style>
