<template>
  <div class="dashboard-page">
    <!-- Quick Stats Grid -->
    <div class="stats-grid">
      <StatCard 
        title="Выручка сегодня" 
        :value="formatCurrency(stats.revenue)" 
        :icon="TrendingUp" 
        colorClass="sky"
        :trend="12.5"
      />
      <StatCard 
        title="Расходы сегодня" 
        :value="formatCurrency(stats.expenses)" 
        :icon="TrendingDown" 
        colorClass="rose"
        :trend="-4.2"
      />
      <StatCard 
        title="Чистая прибыль" 
        :value="formatCurrency(stats.profit)" 
        :icon="DollarSign" 
        colorClass="emerald"
      />
      <StatCard 
        title="Продано блюд" 
        :value="stats.sold_count" 
        :icon="ShoppingBag" 
        colorClass="amber"
      />
    </div>

    <!-- Main Analytics Grid -->
    <div class="analytics-layout mt-4">
      <!-- Big Chart Container -->
      <div class="card p-card chart-hero">
        <div class="section-header">
          <div class="title-meta">
            <h3 class="section-title">Аналитика выручки</h3>
            <p class="t-small">Динамика за последние 7 дней</p>
          </div>
          <div class="chart-indicators">
            <div class="indicator-item">
              <span class="dot primary"></span>
              <span class="t-small">Текущий период</span>
            </div>
          </div>
        </div>
        <div class="chart-wrapper">
          <apexchart 
            height="380" 
            type="area" 
            :options="lineChartOptions" 
            :series="lineChartSeries" 
          />
        </div>
      </div>

      <!-- Side Column -->
      <div class="side-column">
        <!-- Top Products List -->
        <div class="card p-card products-list-card">
          <h3 class="section-title mb-1">Топ товаров</h3>
          <p class="t-small mb-3">По количеству продаж</p>
          
          <div class="products-stack">
            <div v-for="(prod, idx) in stats.top_products" :key="idx" class="product-row">
              <div class="product-rank">{{ idx + 1 }}</div>
              <div class="product-details">
                <span class="product-name">{{ prod.name }}</span>
                <span class="product-meta t-small">Еда • Горячее</span>
              </div>
              <div class="product-value">
                <span class="count">{{ prod.value }}</span>
                <span class="t-small">шт</span>
              </div>
            </div>
            <div v-if="stats.top_products.length === 0" class="empty-list t-small">
              Нет данных о продажах
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Row: Expenses Distribution -->
    <div class="card p-card distribution-card mt-4">
      <div class="flex justify-between items-start mb-4">
        <div>
          <h3 class="section-title">Структура расходов</h3>
          <p class="t-small">Распределение по категориям за месяц</p>
        </div>
        <button class="p-btn p-btn-ghost btn-sm">Детальный отчет</button>
      </div>

      <div class="distribution-grid">
        <div class="donut-chart-box">
          <apexchart 
            width="340" 
            type="donut" 
            :options="pieChartOptions" 
            :series="pieChartSeries" 
          />
        </div>
        
        <div class="distribution-legend">
          <div v-for="(val, idx) in stats.pie_chart.labels" :key="idx" class="legend-card">
            <div class="legend-color-tag" :style="{ backgroundColor: pieColors[idx] }"></div>
            <div class="legend-info">
              <span class="legend-name">{{ val }}</span>
              <span class="legend-amount font-black">{{ formatCurrency(stats.pie_chart.data[idx]) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { TrendingUp, TrendingDown, DollarSign, ShoppingBag } from 'lucide-vue-next'
import StatCard from '../components/StatCard.vue'
import api from '../api'

const stats = ref({
  revenue: 0,
  expenses: 0,
  profit: 0,
  sold_count: 0,
  top_products: [],
  line_chart: { labels: [], data: [] },
  pie_chart: { labels: [], data: [] }
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(val)
}

const pieColors = ['#007AFF', '#34C759', '#FFCC00', '#FF3B30', '#5856D6']

const lineChartSeries = computed(() => [{
  name: 'Выручка',
  data: stats.value.line_chart.data
}])

const lineChartOptions = {
  chart: { 
    toolbar: { show: false }, 
    fontFamily: 'Inter',
    sparkline: { enabled: false }
  },
  stroke: { curve: 'smooth', width: 3, lineCap: 'round' },
  colors: ['#007AFF'],
  fill: { 
    type: 'gradient', 
    gradient: { 
      shadeIntensity: 1, 
      opacityFrom: 0.2, 
      opacityTo: 0.02, 
      stops: [0, 90, 100] 
    } 
  },
  xaxis: { 
    categories: stats.value.line_chart.labels, 
    axisBorder: { show: false }, 
    axisTicks: { show: false },
    labels: { style: { colors: '#86868B', fontSize: '11px' } }
  },
  yaxis: { show: false },
  dataLabels: { enabled: false },
  grid: { 
    borderColor: 'rgba(0,0,0,0.03)', 
    strokeDashArray: 4,
    padding: { left: 0, right: 0 }
  },
  tooltip: { theme: 'light', x: { show: false } }
}

const pieChartSeries = computed(() => stats.value.pie_chart.data)
const pieChartOptions = computed(() => ({
  labels: stats.value.pie_chart.labels,
  colors: pieColors,
  legend: { show: false },
  dataLabels: { enabled: false },
  plotOptions: { 
    pie: { 
      donut: { 
        size: '80%', 
        labels: { 
          show: true, 
          name: { show: true, fontSize: '12px', fontWeight: 600, color: '#86868B' },
          value: { show: true, fontSize: '24px', fontWeight: 800, color: '#1D1D1F' },
          total: { show: true, label: 'Всего', color: '#86868B' } 
        } 
      } 
    } 
  },
  stroke: { width: 4, colors: ['#fff'] }
}))

onMounted(async () => {
  try {
    const { data } = await api.get('/analytics/daily')
    stats.value = data
  } catch (e) {
    console.error("Dashboard data load failed", e)
  }
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

@media (max-width: 1200px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .stats-grid { grid-template-columns: 1fr; }
}

.analytics-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 32px;
}

@media (max-width: 1200px) {
  .analytics-layout { grid-template-columns: 1fr; }
}

.chart-hero {
  padding: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.indicator-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot.primary { background: var(--p-primary); }

.chart-wrapper {
  margin: 0 -10px;
}

/* Products Column */
.products-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
}

.product-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.product-rank {
  width: 32px;
  height: 32px;
  background: #F5F5F7;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
}

.product-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-size: 14px;
  font-weight: 700;
}

.product-value {
  text-align: right;
  display: flex;
  flex-direction: column;
}

.product-value .count {
  font-size: 16px;
  font-weight: 800;
}

/* Distribution Section */
.distribution-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 60px;
  align-items: center;
  margin-top: 24px;
}

@media (max-width: 1024px) {
  .distribution-grid { grid-template-columns: 1fr; justify-items: center; gap: 32px; }
}

.distribution-legend {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  width: 100%;
}

@media (max-width: 640px) {
  .distribution-legend { grid-template-columns: 1fr; }
}

.legend-card {
  padding: 16px 20px;
  background: #FBFBFC;
  border-radius: 16px;
  border: 1px solid var(--p-border);
  display: flex;
  align-items: center;
  gap: 12px;
}

.legend-color-tag {
  width: 4px;
  height: 24px;
  border-radius: 2px;
}

.legend-info {
  display: flex;
  flex-direction: column;
}

.legend-name {
  font-size: 12px;
  color: var(--p-text-sec);
  font-weight: 600;
}

.legend-amount {
  font-size: 15px;
}

.mb-1 { margin-bottom: 4px; }
.mb-3 { margin-bottom: 24px; }
.mb-4 { margin-bottom: 32px; }
.mt-4 { margin-top: 32px; }
.font-black { font-weight: 900; }
</style>
