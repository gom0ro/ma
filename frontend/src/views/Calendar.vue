<template>
  <div class="calendar-view animate-view">
    <div class="calendar-layout">
      <!-- Calendar Main Section -->
      <div class="calendar-main card p-card">
        <div class="calendar-header">
          <div class="month-nav">
            <button @click="prevMonth" class="nav-btn"><ChevronLeft /></button>
            <h2 class="month-title">{{ monthName }} {{ currentYear }}</h2>
            <button @click="nextMonth" class="nav-btn"><ChevronRight /></button>
          </div>
          <button @click="goToToday" class="p-btn p-btn-ghost">Сегодня</button>
        </div>

        <div class="calendar-grid">
          <div v-for="day in weekDays" :key="day" class="weekday-label">{{ day }}</div>
          
          <div 
            v-for="date in calendarDates" 
            :key="date.iso"
            :class="['calendar-day', { 
              'other-month': !date.isCurrentMonth,
              'is-today': date.isToday,
              'is-selected': selectedDate === date.iso,
              'has-data': date.hasData
            }]"
            @click="selectDate(date.iso)"
          >
            <span class="day-number">{{ date.day }}</span>
            <div v-if="date.hasData" class="day-dot"></div>
          </div>
        </div>
      </div>

      <!-- Day Details Sidebar -->
      <aside class="day-details">
        <div v-if="selectedDate" class="card p-card sticky-details">
          <div class="details-header">
            <h3 class="section-title">{{ formatFullDate(selectedDate) }}</h3>
            <p class="t-small">Статистика за день</p>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Загрузка данных...</p>
          </div>

          <div v-else class="stats-list">
            <div class="stat-item primary">
              <div class="stat-icon"><TrendingUp size="20" /></div>
              <div class="stat-info">
                <p class="t-tiny">Выручка</p>
                <p class="stat-value">{{ formatCurrency(dayStats.revenue) }}</p>
              </div>
            </div>

            <div class="stat-item error">
                <div class="stat-icon"><TrendingDown size="20" /></div>
                <div class="stat-info">
                  <p class="t-tiny">Расходы</p>
                  <p class="stat-value">{{ formatCurrency(dayStats.expenses) }}</p>
                </div>
            </div>

            <div class="stat-item success">
                <div class="stat-icon"><DollarSign size="20" /></div>
                <div class="stat-info">
                  <p class="t-tiny">Прибыль</p>
                  <p class="stat-value">{{ formatCurrency(dayStats.profit) }}</p>
                </div>
            </div>

            <div class="stat-divider"></div>

            <div class="top-products">
              <p class="t-small mb-3">Топ товаров</p>
              <div v-for="p in dayStats.top_products" :key="p.name" class="top-p-item">
                <span class="p-name">{{ p.name }}</span>
                <span class="p-count">{{ p.value }} шт.</span>
              </div>
              <div v-if="dayStats.top_products.length === 0" class="t-small opacity-50">Нет продаж за этот день</div>
            </div>
          </div>
        </div>
        <div v-else class="card p-card empty-details">
          <div class="empty-icon"><CalendarIcon size="48" /></div>
          <h3>Выберите дату</h3>
          <p>Нажмите на любой день в календаре, чтобы увидеть подробную статистику</p>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { 
    ChevronLeft, 
    ChevronRight, 
    TrendingUp, 
    TrendingDown, 
    DollarSign,
    Calendar as CalendarIcon
} from 'lucide-vue-next'
import api from '../api'

const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

const currentDate = ref(new Date())
const selectedDate = ref(new Date().toISOString().split('T')[0])
const dayStats = ref({ revenue: 0, expenses: 0, profit: 0, top_products: [] })
const monthSummary = ref({})
const loading = ref(false)

const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())
const monthName = computed(() => monthNames[currentMonth.value])

const calendarDates = computed(() => {
    const year = currentYear.value
    const month = currentMonth.value
    
    const firstDayOfMonth = new Date(year, month, 1)
    const lastDayOfMonth = new Date(year, month + 1, 0)
    
    // Get padding for previous month
    let startPadding = firstDayOfMonth.getDay() - 1
    if (startPadding === -1) startPadding = 6
    
    const dates = []
    
    // Previous month dates
    const prevMonthLastDay = new Date(year, month, 0).getDate()
    for (let i = startPadding - 1; i >= 0; i--) {
        const d = new Date(year, month - 1, prevMonthLastDay - i)
        const iso = d.toISOString().split('T')[0]
        dates.push({
            day: d.getDate(),
            iso,
            isCurrentMonth: false,
            isToday: isToday(d),
            hasData: !!monthSummary.value[iso]
        })
    }
    
    // Current month dates
    for (let i = 1; i <= lastDayOfMonth.getDate(); i++) {
        const d = new Date(year, month, i)
        const iso = d.toISOString().split('T')[0]
        dates.push({
            day: i,
            iso,
            isCurrentMonth: true,
            isToday: isToday(d),
            hasData: !!monthSummary.value[iso]
        })
    }
    
    // Next month padding
    const remaining = 42 - dates.length
    for (let i = 1; i <= remaining; i++) {
        const d = new Date(year, month + 1, i)
        const iso = d.toISOString().split('T')[0]
        dates.push({
            day: i,
            iso,
            isCurrentMonth: false,
            isToday: isToday(d),
            hasData: !!monthSummary.value[iso]
        })
    }
    
    return dates
})

const isToday = (date) => {
    const today = new Date()
    return date.getDate() === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
}

const prevMonth = () => {
    currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
    fetchMonthSummary()
}

const nextMonth = () => {
    currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
    fetchMonthSummary()
}

const goToToday = () => {
    currentDate.value = new Date()
    selectDate(new Date().toISOString().split('T')[0])
    fetchMonthSummary()
}

const selectDate = (iso) => {
    selectedDate.value = iso
    fetchDayStats(iso)
}

const fetchMonthSummary = async () => {
    try {
        const { data } = await api.get(`/analytics/calendar-summary?year=${currentYear.value}&month=${currentMonth.value + 1}`)
        monthSummary.value = data
    } catch (e) {
        console.error(e)
    }
}

const fetchDayStats = async (iso) => {
    loading.value = true
    try {
        const { data } = await api.get(`/analytics/daily?target_date=${iso}`)
        dayStats.value = data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

const formatCurrency = (val) => new Intl.NumberFormat('ru-KZ', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(val)

const formatFullDate = (iso) => {
    return new Date(iso).toLocaleDateString('ru-RU', { 
        day: 'numeric', month: 'long', year: 'numeric' 
    })
}

onMounted(() => {
    fetchMonthSummary()
    if (selectedDate.value) {
        fetchDayStats(selectedDate.value)
    }
})
</script>

<style scoped>
.calendar-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

@media (max-width: 1200px) {
  .calendar-layout { grid-template-columns: 1fr; }
}

.calendar-main {
  padding: 40px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.month-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.month-title {
  min-width: 200px;
  text-align: center;
  font-size: 24px;
}

.nav-btn {
  background: #F2F2F7;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--p-transition);
}

.nav-btn:hover { background: #E5E5EA; }

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.weekday-label {
  text-align: center;
  font-size: 11px;
  font-weight: 800;
  color: var(--p-text-sec);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding-bottom: 16px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  cursor: pointer;
  transition: var(--p-transition);
  position: relative;
  font-weight: 600;
}

.calendar-day:hover { background: #F2F2F7; }

.calendar-day.other-month {
  color: #C7C7CC;
}

.calendar-day.is-today {
  color: var(--p-primary);
}

.calendar-day.is-selected {
  background: var(--p-text);
  color: white;
}

.day-dot {
  width: 4px;
  height: 4px;
  background: var(--p-primary);
  border-radius: 50%;
  position: absolute;
  bottom: 10px;
}

.calendar-day.is-selected .day-dot {
  background: white;
}

/* Details Sidebar */
.day-details .sticky-details {
  position: sticky;
  top: 40px;
}

.details-header { margin-bottom: 32px; }

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-item.primary { background: #F0F7FF; color: #007AFF; }
.stat-item.primary .stat-icon { background: rgba(0,122,255,0.1); }

.stat-item.error { background: #FFF1F0; color: #FF3B30; }
.stat-item.error .stat-icon { background: rgba(255,59,48,0.1); }

.stat-item.success { background: #F2FBF4; color: #34C759; }
.stat-item.success .stat-icon { background: rgba(52,199,89,0.1); }

.stat-value {
  font-size: 18px;
  font-weight: 800;
  margin-top: 2px;
}

.stat-divider {
  height: 1px;
  background: var(--p-border);
  margin: 16px 0;
}

.top-p-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #F2F2F7;
  font-size: 14px;
}

.top-p-item:last-child { border-bottom: none; }

.p-name { font-weight: 600; color: var(--p-text); }
.p-count { color: var(--p-text-sec); }

.empty-details {
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: var(--p-text-sec);
  padding: 40px;
}

.empty-icon {
  margin-bottom: 24px;
  opacity: 0.1;
}

.loading-state {
  padding: 40px 0;
  text-align: center;
  color: var(--p-text-sec);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #F2F2F7;
  border-top-color: var(--p-primary);
  border-radius: 50%;
  animation: rotate 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes rotate {
  to { transform: rotate(360deg); }
}

.mb-3 { margin-bottom: 12px; }
.opacity-50 { opacity: 0.5; }
</style>
