<template>
  <div class="cashier-view animate-view">
    <div class="cash-grid">
      <!-- Left Column: Summary & History -->
      <div class="cash-main-col">
        <!-- Balance Hero Card -->
        <div class="card p-card balance-hero">
          <div class="balance-content">
            <p class="t-small white-text">Средства в кассе</p>
            <h1 class="balance-total">{{ formatCurrency(balanceRes.balance) }}</h1>
            
            <div class="sub-stats mt-4">
              <div class="sub-stat-item">
                <p class="t-tiny white-text opacity-70">Продажи (+)</p>
                <p class="sub-stat-val text-success-light">{{ formatCurrency(balanceRes.total_sales) }}</p>
              </div>
              <div class="v-divider"></div>
              <div class="sub-stat-item">
                <p class="t-tiny white-text opacity-70">Закупки (-)</p>
                <p class="sub-stat-val text-error-light">{{ formatCurrency(balanceRes.total_purchases) }}</p>
              </div>
            </div>
          </div>
          <div class="balance-icon hide-sm">
            <Wallet size="60" />
          </div>
        </div>

        <!-- History Card -->
        <div class="card p-card history-card mt-4">
          <div class="section-header mb-4">
            <h3 class="section-title">История операций</h3>
          </div>
          
          <div class="p-table-container">
            <table class="p-table">
              <thead>
                <tr>
                  <th>Дата / Время</th>
                  <th>Описание</th>
                  <th class="text-right">Сумма</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="op in history" :key="op.id">
                  <td>
                    <p class="font-bold text-sm">{{ formatDate(op.date) }}</p>
                    <p class="t-tiny">{{ formatTime(op.date) }}</p>
                  </td>
                  <td>
                    <span class="op-desc">{{ op.description }}</span>
                  </td>
                  <td :class="['text-right font-black', op.type === 'INCOME' ? 'text-success' : 'text-error']">
                    {{ op.type === 'INCOME' ? '+' : '-' }} {{ formatCurrency(op.amount) }}
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="history.length === 0" class="empty-state">История операций пуста</div>
          </div>
        </div>
      </div>

      <!-- Right Column: Add Operation Form -->
      <aside class="cash-side-col">
        <div class="card p-card form-sticky">
          <h3 class="section-title">Новая запись</h3>
          <p class="t-small mb-4">Укажите детали транзакции</p>
          
          <form @submit.prevent="submitOp" class="op-form">
            <div class="form-group">
              <label class="t-small">Тип операции</label>
              <div class="type-pills">
                <button 
                  type="button"
                  @click="newOp.type = 'INCOME'" 
                  :class="['type-pill income', { active: newOp.type === 'INCOME' }]"
                >Приход</button>
                <button 
                  type="button"
                  @click="newOp.type = 'OUTCOME'" 
                  :class="['type-pill outcome', { active: newOp.type === 'OUTCOME' }]"
                >Списание</button>
              </div>
            </div>
            
            <div class="form-group">
              <label class="t-small">Сумма (₸)</label>
              <input 
                v-model.number="newOp.amount" 
                type="number" 
                class="p-input amount-input" 
                placeholder="0.00" 
                required
                min="0.01"
              />
            </div>
            
            <div class="form-group">
              <label class="t-small">Комментарий</label>
              <textarea 
                v-model="newOp.description" 
                class="p-input textarea" 
                placeholder="Например: покупка хозтоваров..." 
                rows="4"
                required
              ></textarea>
            </div>
            
            <button class="p-btn p-btn-primary full-width mt-2 py-4">
              Сохранить операцию
            </button>
          </form>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Wallet } from 'lucide-vue-next'
import api from '../api'

const balanceRes = ref({ balance: 0, total_purchases: 0, total_sales: 0 })
const history = ref([])
const newOp = ref({ type: 'INCOME', amount: 0, description: '' })

const fetchAll = async () => {
    try {
        const [bal, hist] = await Promise.all([
            api.get('/analytics/cash-summary'),
            api.get('/data/cash/history')
        ])
        balanceRes.value = bal.data
        history.value = hist.data
    } catch (e) {
        console.error(e)
    }
}

const submitOp = async () => {
  if (newOp.value.amount <= 0) return
  try {
    await api.post('/data/cash', newOp.value)
    newOp.value = { type: 'INCOME', amount: 0, description: '' }
    fetchAll()
  } catch (e) {
    console.error(e)
  }
}

const formatCurrency = (val) => new Intl.NumberFormat('ru-KZ', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(val)
const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('ru-RU')
const formatTime = (dateStr) => new Date(dateStr).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })

onMounted(fetchAll)
</script>

<style scoped>
.cash-grid {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

@media (max-width: 1200px) {
  .cash-grid { grid-template-columns: 1fr; }
}

.balance-hero {
  background: var(--p-text);
  color: white;
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance-total {
  font-size: 52px;
  letter-spacing: -0.05em;
  margin-top: 8px;
}

.sub-stats {
  display: flex;
  gap: 32px;
}

.sub-stat-val {
  font-size: 18px;
  font-weight: 800;
  margin-top: 4px;
}

.v-divider {
  width: 1px;
  background: rgba(255,255,255,0.1);
}

.balance-icon { opacity: 0.2; }

.white-text { color: white; }
.opacity-70 { opacity: 0.7; }
.text-success-light { color: #58E681; }
.text-error-light { color: #FF6B6B; }

.history-card { padding: 40px; }

.op-desc { color: var(--p-text-sec); font-size: 14px; font-weight: 500; }
.text-success { color: var(--p-success); }
.text-error { color: var(--p-error); }

/* Form Sidebar */
.form-sticky {
  position: sticky;
  top: 40px;
  padding: 32px;
}

.op-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.type-pills {
  display: flex;
  background: #F2F2F7;
  padding: 4px;
  border-radius: 12px;
  gap: 4px;
}

.type-pill {
  flex: 1;
  border: none;
  padding: 10px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--p-transition);
  color: var(--p-text-sec);
  background: transparent;
}

.type-pill.active.income {
  background: white;
  color: var(--p-success);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.type-pill.active.outcome {
  background: white;
  color: var(--p-error);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.amount-input {
  font-size: 24px;
  font-weight: 800;
  text-align: center;
}

.textarea {
  resize: none;
  font-family: inherit;
}

.full-width { width: 100%; }
.mt-2 { margin-top: 16px; }
.py-4 { padding-top: 20px; padding-bottom: 20px; }
.mb-4 { margin-bottom: 32px; }

@media (max-width: 768px) {
  .balance-hero { padding: 32px 24px; }
  .balance-total { font-size: 36px; }
  .sub-stats { gap: 16px; }
  .history-card { padding: 24px; }
}

.hide-sm { display: block; }
@media (max-width: 640px) {
  .hide-sm { display: none; }
}
</style>
