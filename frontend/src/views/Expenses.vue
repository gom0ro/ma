<template>
  <div class="expenses-view">
    <!-- Quick Stats -->
    <div class="summary-section">
      <div class="card p-card summary-card">
        <div class="summary-info">
          <p class="t-small white-text">Затраты за период</p>
          <h2 class="summary-total">{{ formatCurrency(totalPeriod) }}</h2>
        </div>
        <div class="summary-icon hide-sm">
          <Receipt size="40" />
        </div>
      </div>
    </div>

    <!-- Suppliers Section -->
    <div class="card p-card suppliers-section mt-4">
      <div class="section-header flex-column-mobile gap-2">
        <h3 class="section-title">Поставщики</h3>
        <div class="supplier-add-form full-width-mobile">
          <input 
            v-model="newSupplier.name" 
            placeholder="Новый поставщик" 
            class="p-input input-sm" 
            @keyup.enter="addSupplier" 
          />
          <button @click="addSupplier" class="p-btn p-btn-primary p-btn-sm">Добавить</button>
        </div>
      </div>
      <div class="suppliers-cloud mt-3">
        <div v-for="s in suppliers" :key="s.id" class="supplier-pill">
          {{ s.name }}
        </div>
        <div v-if="suppliers.length === 0" class="empty-msg">Список пуст</div>
      </div>
    </div>

    <!-- Actions & Filters -->
    <div class="actions-row mt-4">
      <div class="filters-group card p-card flex-column-mobile">
        <div class="date-inputs full-width-mobile">
          <input type="date" v-model="filters.start" class="p-input input-minimal" />
          <span class="date-sep">→</span>
          <input type="date" v-model="filters.end" class="p-input input-minimal" />
        </div>
        <div class="v-sep hide-sm"></div>
        <select v-model="filters.supplier" class="p-input input-minimal select-box full-width-mobile">
          <option value="">Все поставщики</option>
          <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
        <button @click="fetchExpenses" class="search-btn full-width-mobile">
          <Search size="18" />
          <span class="show-sm ml-2">Найти</span>
        </button>
      </div>

      <button @click="showAddModal = true" class="p-btn p-btn-primary btn-add full-width-mobile">
        <Plus size="20" />
        <span>Новый расход</span>
      </button>
    </div>

    <!-- Table -->
    <div class="card p-card table-card mt-4 no-padding-mobile">
      <div class="p-table-container">
        <table class="p-table">
          <thead>
            <tr>
              <th>Товар / Инфо</th>
              <th class="hide-sm">Поставщик</th>
              <th class="hide-sm">Категория</th>
              <th class="text-right">Сумма</th>
              <th class="text-right hide-sm">Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="exp in expenses" :key="exp.id">
              <td>
                <p class="font-bold text-base">{{ exp.name }}</p>
                <p class="t-small block-mobile mt-1">{{ exp.quantity }} шт × {{ formatCurrency(exp.price) }}</p>
                <div class="show-sm mt-2 flex gap-1 items-center">
                   <span class="category-badge-sm">{{ exp.category }}</span>
                   <span class="t-tiny">• {{ exp.supplier.name }}</span>
                </div>
              </td>
              <td class="supplier-cell hide-sm">{{ exp.supplier.name }}</td>
              <td class="hide-sm">
                <span class="category-badge">{{ exp.category }}</span>
              </td>
              <td class="text-right">
                <p class="font-black text-lg">{{ formatCurrency(exp.total_amount) }}</p>
                <p class="show-sm t-tiny mt-1">{{ formatDate(exp.date) }}</p>
              </td>
              <td class="text-right date-cell hide-sm">{{ formatDate(exp.date) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="expenses.length === 0" class="empty-state">Нет данных</div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showAddModal" class="p-modal-overlay" @click.self="showAddModal = false">
      <div class="p-modal-card">
        <h2 class="modal-title">Новый расход</h2>
        <form @submit.prevent="addExpense" class="modal-form">
          <div class="form-item">
            <label class="t-small">Название товара</label>
            <input v-model="newExpense.name" placeholder="Название" class="p-input" required />
          </div>
          <div class="form-row">
            <div class="form-item">
              <label class="t-small">Количество</label>
              <input v-model.number="newExpense.quantity" type="number" step="0.01" class="p-input" required />
            </div>
            <div class="form-item">
              <label class="t-small">Цена</label>
              <input v-model.number="newExpense.price" type="number" step="0.01" class="p-input" required />
            </div>
          </div>
          <div class="form-item">
            <label class="t-small">Поставщик</label>
            <select v-model="newExpense.supplier_id" class="p-input" required>
              <option disabled value="">Выберите...</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="form-item">
            <label class="t-small">Категория</label>
            <input v-model="newExpense.category" placeholder="Еда, бытовая химия..." class="p-input" required />
          </div>
          <div class="form-item">
            <label class="t-small">Дата</label>
            <input v-model="newExpense.date" type="datetime-local" class="p-input" required />
          </div>
          <div class="modal-btns mt-4">
            <button type="button" @click="showAddModal = false" class="p-btn p-btn-ghost">Отмена</button>
            <button class="p-btn p-btn-primary">Сохранить</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Plus, Search, Receipt } from 'lucide-vue-next'
import api from '../api'

const expenses = ref([])
const suppliers = ref([])
const showAddModal = ref(false)
const filters = ref({ start: '', end: '', supplier: '' })
const newExpense = ref({ 
    name: '', 
    quantity: 0, 
    price: 0, 
    supplier_id: '', 
    category: '',
    date: new Date().toISOString().slice(0, 16)
})
const newSupplier = ref({ name: '' })

const fetchSuppliers = async () => {
    const { data } = await api.get('/data/suppliers')
    suppliers.value = data
}

const addSupplier = async () => {
  if (!newSupplier.value.name.trim()) return
  try {
    await api.post('/data/suppliers', newSupplier.value)
    newSupplier.value.name = ''
    fetchSuppliers()
  } catch (e) {
    console.error(e)
  }
}

const fetchExpenses = async () => {
    let url = '/data/expenses?'
    if (filters.value.start) url += `start_date=${filters.value.start}&`
    if (filters.value.end) url += `end_date=${filters.value.end}&`
    if (filters.value.supplier) url += `supplier_id=${filters.value.supplier}`
    const { data } = await api.get(url)
    expenses.value = data
}

const addExpense = async () => {
  await api.post('/data/expenses', newExpense.value)
  showAddModal.value = false
  newExpense.value = { 
    name: '', 
    quantity: 0, 
    price: 0, 
    supplier_id: '', 
    category: '',
    date: new Date().toISOString().slice(0, 16)
  }
  fetchExpenses()
}

const totalPeriod = computed(() => expenses.value.reduce((acc, exp) => acc + exp.total_amount, 0))
const formatCurrency = (val) => new Intl.NumberFormat('ru-KZ', { style: 'currency', currency: 'KZT', maximumFractionDigits: 0 }).format(val)
const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('ru-RU')

onMounted(async () => {
  await Promise.all([fetchExpenses(), fetchSuppliers()])
})
</script>

<style scoped>
.summary-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--p-text);
  color: white;
}

.summary-total {
  font-size: 36px;
  margin-top: 4px;
}

.summary-icon { opacity: 0.2; }

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.suppliers-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.supplier-pill {
  padding: 8px 16px;
  background: #F2F2F7;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--p-text);
}

.supplier-add-form {
  display: flex;
  gap: 8px;
}

.input-sm { padding: 8px 16px; width: 200px; }
.p-btn-sm { padding: 8px 16px; font-size: 13px; }

.actions-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 16px;
  align-items: center;
}

@media (max-width: 768px) {
  .actions-row { grid-template-columns: 1fr; }
}

.filters-group {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  gap: 16px;
}

@media (max-width: 640px) {
  .filters-group { flex-direction: column; align-items: stretch; }
  .v-sep, .date-sep { display: none; }
}

.date-inputs { display: flex; align-items: center; gap: 8px; flex: 1; }
.input-minimal { background: transparent; padding: 8px; border: none; font-weight: 700; width: auto; }
.input-minimal:focus { box-shadow: none; border-bottom: 2px solid var(--p-primary); border-radius: 0; }
.v-sep { width: 1px; height: 24px; background: var(--p-border); }
.select-box { flex: 1; cursor: pointer; }

.search-btn {
  background: var(--p-text);
  color: white;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-add { height: 52px; padding: 0 32px; font-size: 15px; }

.category-badge {
  padding: 4px 10px;
  background: #F2F2F7;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--p-text-sec);
  text-transform: uppercase;
}

.date-cell { color: var(--p-text-sec); font-size: 13px; }
.supplier-cell { font-weight: 600; color: var(--p-text-sec); }

/* Mobile Helpers */
@media (max-width: 768px) {
  .flex-column-mobile { flex-direction: column; align-items: stretch !important; }
  .full-width-mobile { width: 100% !important; margin-left: 0 !important; }
  .hide-sm { display: none !important; }
  .show-sm { display: flex !important; }
  .no-padding-mobile { padding-left: 0 !important; padding-right: 0 !important; border-radius: 0 !important; border-left: none !important; border-right: none !important; }
  .block-mobile { display: block !important; }
  .mt-1 { margin-top: 4px !important; }
  .mt-2 { margin-top: 8px !important; }
  .mt-3 { margin-top: 12px !important; }
  .ml-2 { margin-left: 8px !important; }
  .text-base { font-size: 15px !important; }
  .text-lg { font-size: 17px !important; }
}

.show-sm { display: none; }
.white-text { color: white; }
.category-badge-sm {
  padding: 2px 8px;
  background: #F2F2F7;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  color: var(--p-text-sec);
  text-transform: uppercase;
}
.t-tiny { font-size: 10px; color: var(--p-text-sec); }
.items-center { align-items: center; }

.empty-state {
  padding: 60px;
  text-align: center;
  color: var(--p-text-sec);
  font-style: italic;
}

/* Modal */
.p-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(8px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.p-modal-card {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-title { margin-bottom: 32px; font-size: 24px; }
.modal-form { display: flex; flex-direction: column; gap: 20px; }
.form-item { display: flex; flex-direction: column; gap: 8px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.modal-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.text-right { text-align: right; }
.font-bold { font-weight: 700; }
.font-black { font-weight: 900; }
</style>
