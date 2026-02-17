<template>
  <div class="compare-view animate-view">
    <!-- Date Range Selector -->
    <div class="card p-card selector-card">
      <div class="selector-grid">
        <div class="date-picker-box">
          <label class="t-small">Первая дата</label>
          <input type="date" v-model="date1" class="p-input" />
        </div>
        <div class="vs-divider hide-sm">
          <div class="line"></div>
          <span class="vs-text">VS</span>
          <div class="line"></div>
        </div>
        <div class="date-picker-box">
          <label class="t-small">Вторая дата</label>
          <input type="date" v-model="date2" class="p-input" />
        </div>
        <button @click="compare" class="p-btn p-btn-primary compare-trigger">
          <ArrowLeftRight size="18" />
          <span>Сравнить</span>
        </button>
      </div>
    </div>

    <!-- Comparison Results -->
    <div v-if="result" class="results-layout mt-4 animate-view">
      <div class="grid grid-3 gap-2">
        <!-- Revenue Comparison -->
        <div class="card p-card comparison-card">
          <div class="flex justify-between mb-4">
            <p class="t-small">Выручка</p>
            <div :class="['trend-pill', result.revenue.diff >= 0 ? 'up' : 'down']">
              {{ result.revenue.diff >= 0 ? '+' : '' }}{{ result.revenue.diff }}%
            </div>
          </div>
          
          <div class="comparison-flow">
            <div class="comp-item">
              <span class="comp-date t-tiny">{{ formatDateShort(date1) }}</span>
              <span class="comp-val">{{ formatCurrency(result.revenue.val1) }}</span>
            </div>
            <ArrowRight size="16" class="comp-arrow" />
            <div class="comp-item text-right">
              <span class="comp-date t-tiny">{{ formatDateShort(date2) }}</span>
              <span class="comp-val highlighted">{{ formatCurrency(result.revenue.val2) }}</span>
            </div>
          </div>
        </div>

        <!-- Expenses Comparison -->
        <div class="card p-card comparison-card">
          <div class="flex justify-between mb-4">
            <p class="t-small">Расходы</p>
            <div :class="['trend-pill', result.expenses.diff <= 0 ? 'up-good' : 'down-bad']">
              {{ result.expenses.diff >= 0 ? '+' : '' }}{{ result.expenses.diff }}%
            </div>
          </div>
          
          <div class="comparison-flow">
            <div class="comp-item">
              <span class="comp-date t-tiny">{{ formatDateShort(date1) }}</span>
              <span class="comp-val">{{ formatCurrency(result.expenses.val1) }}</span>
            </div>
            <ArrowRight size="16" class="comp-arrow" />
            <div class="comp-item text-right">
              <span class="comp-date t-tiny">{{ formatDateShort(date2) }}</span>
              <span class="comp-val highlighted">{{ formatCurrency(result.expenses.val2) }}</span>
            </div>
          </div>
        </div>

        <!-- Profit Comparison -->
        <div class="card p-card comparison-card">
          <div class="flex justify-between mb-4">
            <p class="t-small">Прибыль</p>
            <div :class="['trend-pill', result.profit.diff >= 0 ? 'up' : 'down']">
              {{ result.profit.diff >= 0 ? '+' : '' }}{{ result.profit.diff }}%
            </div>
          </div>
          
          <div class="comparison-flow">
            <div class="comp-item">
              <span class="comp-date t-tiny">{{ formatDateShort(date1) }}</span>
              <span class="comp-val">{{ formatCurrency(result.profit.val1) }}</span>
            </div>
            <ArrowRight size="16" class="comp-arrow" />
            <div class="comp-item text-right">
              <span class="comp-date t-tiny">{{ formatDateShort(date2) }}</span>
              <span class="comp-val highlighted">{{ formatCurrency(result.profit.val2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Comparison Chart -->
      <div class="card p-card chart-comparison-card mt-5">
        <div class="section-header mb-4">
          <h3 class="section-title">Визуальное сопоставление</h3>
          <p class="t-small">Сравнение основных метрик по выбранным датам</p>
        </div>
        <div class="chart-box">
          <apexchart height="380" type="bar" :options="chartOptions" :series="chartSeries" />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state-view card p-card mt-4">
       <div class="empty-content">
          <BarChart3 size="60" class="opacity-10" />
          <p class="mt-2 font-bold">Выберите даты для анализа</p>
          <p class="t-small">Нажмите кнопку «Сравнить», чтобы увидеть результат</p>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowLeftRight, ArrowRight, BarChart3 } from 'lucide-vue-next'
import api from '../api'

const today = new Date().toISOString().split('T')[0]
const date1 = ref(today)
const date2 = ref(today)
const result = ref(null)

const compare = async () => {
    try {
        const { data } = await api.get(`/analytics/compare?date1=${date1.value}&date2=${date2.value}`)
        result.value = data
    } catch (e) {
        console.error("Comparison failed", e)
    }
}

const formatCurrency = (val) => new Intl.NumberFormat('ru-KZ', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(val)
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' })

const chartSeries = computed(() => [
  { name: formatDateShort(date1.value), data: [result.value?.revenue.val1, result.value?.expenses.val1, result.value?.profit.val1] },
  { name: formatDateShort(date2.value), data: [result.value?.revenue.val2, result.value?.expenses.val2, result.value?.profit.val2] }
])

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, fontFamily: 'Inter' },
  plotOptions: { 
    bar: { 
      horizontal: false, 
      columnWidth: '50%', 
      borderRadius: 8,
      dataLabels: { position: 'top' }
    } 
  },
  colors: ['#F2F2F7', '#007AFF'],
  xaxis: { 
    categories: ['Доход', 'Расход', 'Прибыль'],
    axisBorder: { show: false },
    axisTicks: { show: false }
  },
  yaxis: { show: false },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    fontFamily: 'Inter',
    fontWeight: 700
  },
  dataLabels: { 
    enabled: true, 
    formatter: (val) => val > 0 ? (val/1000).toFixed(0) + 'k' : '',
    offsetY: -30,
    style: { fontSize: '11px', colors: ['#86868B'] }
  },
  grid: { borderColor: 'rgba(0,0,0,0.03)', strokeDashArray: 4 },
  tooltip: { theme: 'light' }
}))
</script>

<style scoped>
.selector-card { padding: 32px 40px; }

.selector-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto;
  align-items: end;
  gap: 32px;
}

.date-picker-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.vs-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: center;
  padding-bottom: 8px;
}

.line {
  width: 1px;
  height: 12px;
  background: var(--p-border);
}

.vs-text {
  font-size: 11px;
  font-weight: 800;
  color: var(--p-text-sec);
  margin: 4px 0;
}

.compare-trigger {
  height: 52px;
  padding: 0 32px;
}

/* Results */
.comparison-card {
  padding: 32px;
}

.trend-pill {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
}

.trend-pill.up { background: #E8F7ED; color: #34C759; }
.trend-pill.down { background: #FFF0EF; color: #FF3B30; }
.trend-pill.up-good { background: #FFF0EF; color: #FF3B30; } /* expenses up */
.trend-pill.down-bad { background: #E8F7ED; color: #34C759; } /* expenses down */

.comparison-flow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
}

.comp-item {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.comp-date { color: var(--p-text-sec); margin-bottom: 2px; }
.comp-val { font-size: 18px; font-weight: 700; color: var(--p-text-sec); }
.comp-val.highlighted { font-size: 22px; font-weight: 900; color: var(--p-text); }

.comp-arrow { color: var(--p-border); margin: 0 12px; }

.chart-comparison-card { padding: 48px; }

.empty-state-view {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--p-text-sec);
}

.opacity-10 { opacity: 0.1; }

@media (max-width: 1024px) {
  .selector-grid { grid-template-columns: 1fr 1fr; gap: 24px; }
  .vs-divider { display: none; }
  .compare-trigger { grid-column: span 2; }
}

@media (max-width: 768px) {
  .chart-comparison-card { padding: 24px; }
  .grid-3 { grid-template-columns: 1fr; }
  .comp-val { font-size: 16px; }
  .comp-val.highlighted { font-size: 18px; }
  .selector-grid { grid-template-columns: 1fr; }
  .compare-trigger { grid-column: span 1; }
}
</style>
