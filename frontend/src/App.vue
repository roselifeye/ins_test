<template>
  <div class="app">
    <header class="app-header">
      <div class="title">Inspection Agent 控制台</div>
      <div class="subtitle">依据 PRD 实现多模型对比 + AI 评审团的统一操作界面</div>
    </header>
    <main class="app-body">
      <section class="left"><left-panel /></section>
      <section class="right"><right-panel /></section>
    </main>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
import LeftPanel from './components/LeftPanel.vue';
import RightPanel from './components/RightPanel.vue';
import { useEvaluationStore } from './store/evaluation';

const store = useEvaluationStore();

onMounted(() => {
  store.initialise();
});
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: linear-gradient(180deg, #f5f7fa 0%, #ffffff 40%);
  display: flex;
  flex-direction: column;
}

.app-header {
  padding: 24px 32px 16px;
  background: #1f2d3d;
  color: #ffffff;
}

.title {
  font-size: 24px;
  font-weight: 700;
}

.subtitle {
  margin-top: 4px;
  font-size: 14px;
  opacity: 0.8;
}

.app-body {
  flex: 1;
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
  padding: 24px 32px;
}

.left,
.right {
  height: fit-content;
}
</style>
