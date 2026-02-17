<template>
  <div class="finances-view">
    <!-- Top Statistics Grid with increased gap -->
    <div class="grid grid-3 gap-2">
      <div class="card p-card mini-stat-card">
        <p class="t-small">Выручка (Месяц)</p>
        <h3 class="stat-value text-primary">{{ formatCurrency(summary.monthly_revenue) }}</h3>
      </div>
      <div class="card p-card mini-stat-card">
        <p class="t-small">Расходы (Месяц)</p>
        <h3 class="stat-value text-error">{{ formatCurrency(summary.monthly_expenses) }}</h3>
      </div>
      <div class="card p-card mini-stat-card">
        <p class="t-small">Маржинальность</p>
        <div class="stat-progress-container mt-2">
          <h3 class="stat-value text-success">{{ summary.profit_margin }}%</h3>
          <div class="p-progress-track">
            <div class="p-progress-bar" :style="{ width: summary.profit_margin + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Chart Section with more top margin -->
    <div class="card p-card chart-hero-card mt-5">
      <div class="section-header">
        <div>
          <h3 class="section-title">Финансовый баланс</h3>
          <p class="t-small">Соотношение доходов и расходов за последние 6 месяцев</p>
        </div>
      </div>
      <div class="chart-box mt-4">
        <apexchart 
           height="400" 
           type="line" 
           :options="chartOptions" 
           :series="chartSeries" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'

const summary = ref({
  monthly_revenue: 0,
  monthly_expenses: 0,
  profit_margin: 0,
})

const labels = ref([])
const revenue = ref([])
const expenses = ref([])

const chartSeries = computed(() => [
  { name: 'Доход', data: revenue.value },
  { name: 'Расход', data: expenses.value }
])

const chartOptions = computed(() => ({
  chart: { 
    toolbar: { show: false }, 
    fontFamily: 'Inter',
    zoom: { enabled: false }
  },
  stroke: { curve: 'smooth', width: 4, lineCap: 'round' },
  colors: ['#007AFF', '#FF3B30'],
  xaxis: { 
    categories: labels.value, 
    axisBorder: { show: false }, 
    axisTicks: { show: false },
    labels: { style: { colors: '#86868B', fontSize: '11px' } }
  },
  yaxis: {
    labels: { 
        style: { colors: '#86868B', fontSize: '11px' },
        formatter: (val) => val > 1000 ? (val/1000).toFixed(0) + 'k' : val
    }
  },
  grid: { borderColor: 'rgba(0,0,0,0.03)', strokeDashArray: 4 },
  markers: { size: 0, hover: { size: 6 } },
  tooltip: { theme: 'light' }
}))

const formatCurrency = (val) => new Intl.NumberFormat('ru-KZ', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(val)

onMounted(async () => {
    try {
        const { data } = await api.get('/analytics/monthly')
        summary.value = {
            monthly_revenue: data.monthly_revenue,
            monthly_expenses: data.monthly_expenses,
            profit_margin: data.profit_margin
        }
        labels.value = data.chart.labels
        revenue.value = data.chart.revenue
        expenses.value = data.chart.expenses
    } catch (e) {
        console.error("Finance data load failed", e)
    }
})
</script>

<style scoped>
.mini-stat-card {
  padding: 32px;
}

.stat-value {
  font-size: 26px;
  margin-top: 8px;
}

.text-primary { color: var(--p-primary); }
.text-error { color: var(--p-error); }
.text-success { color: var(--p-success); }

.stat-progress-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.p-progress-track {
  flex: 1;
  height: 8px;
  background: #F2F2F7;
  border-radius: 4px;
  overflow: hidden;
}

.p-progress-bar {
  height: 100%;
  background: var(--p-success);
  border-radius: 4px;
  transition: width 1s ease-out;
}

.chart-hero-card {
  padding: 48px;
}

.mt-5 { margin-top: 48px; }
.mt-2 { margin-top: 16px; }

@media (max-width: 1024px) {
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .chart-hero-card { padding: 24px; }
  .grid-3 { grid-template-columns: 1fr; }
  .stat-progress-container { flex-direction: column; align-items: flex-start; gap: 10px; }
  .p-progress-track { width: 100%; }
}
</style>
