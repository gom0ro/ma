<template>
  <div class="card p-card stat-card">
    <div class="stat-header">
      <div :class="['stat-icon-container', colorClass]">
        <component :is="icon" size="20" />
      </div>
      <div v-if="trend" :class="['trend-indicator', trend >= 0 ? 'up' : 'down']">
        {{ trend >= 0 ? '↑' : '↓' }} {{ Math.abs(trend) }}%
      </div>
    </div>
    <div class="stat-body">
      <p class="t-small">{{ title }}</p>
      <h3 class="stat-value">{{ value }}</h3>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: Object,
  colorClass: String,
  trend: Number
})
</script>

<style scoped>
.stat-card {
  padding: 24px;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.stat-icon-container {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Icon Colors */
.emerald { background: #E8F7ED; color: #34C759; }
.rose { background: #FFF0EF; color: #FF3B30; }
.sky { background: #E8F2FF; color: #007AFF; }
.amber { background: #FFF9E8; color: #FFCC00; }

.trend-indicator {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 8px;
}

.trend-indicator.up { background: #E8F7ED; color: #34C759; }
.trend-indicator.down { background: #FFF0EF; color: #FF3B30; }

.stat-value {
  font-size: 28px;
  margin-top: 4px;
}
</style>
