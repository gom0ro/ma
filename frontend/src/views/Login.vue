<template>
  <div class="login-page">
    <div class="decor blob-1"></div>
    <div class="decor blob-2"></div>

    <div class="login-container animate-view">
      <div class="card p-card login-card">
        <div class="login-header">
          <div class="logo-circle">
            <span>C</span>
          </div>
          <h1 class="logo-title">CanteenPay</h1>
          <p class="t-small">Система управления финансами</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="t-small">Логин</label>
            <input 
              v-model="username"
              type="text" 
              class="p-input"
              placeholder="admin"
              required
            />
          </div>
          <div class="form-group">
            <label class="t-small">Пароль</label>
            <input 
              v-model="password"
              type="password" 
              class="p-input"
              placeholder="••••••••"
              required
            />
          </div>

          <button 
            :disabled="loading"
            class="p-btn p-btn-primary full-width mt-4"
          >
            {{ loading ? 'Авторизация...' : 'Войти в систему' }}
          </button>
        </form>
        
        <div v-if="error" class="error-box mt-4">
          <AlertCircle size="18" />
          <span>{{ error }}</span>
        </div>

        <div class="login-footer mt-4">
          <p class="t-tiny opacity-50">Если вы забыли пароль, свяжитесь с системным администратором</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { AlertCircle } from 'lucide-vue-next'

const username = ref('admin')
const password = ref('admin123')
const loading = ref(false)
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    if (e.response?.status === 401) {
      error.value = 'Неверный логин или пароль. Попробуйте admin / admin123'
    } else {
      error.value = 'Ошибка сервера. Проверьте соединение.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--p-bg);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

.decor {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.1;
  z-index: 0;
}

.blob-1 {
  top: -100px;
  left: -200px;
  width: 600px;
  height: 600px;
  background: var(--p-primary);
}

.blob-2 {
  bottom: -100px;
  right: -200px;
  width: 600px;
  height: 600px;
  background: var(--p-accent);
}

.login-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 2;
}

.login-card {
  padding: 48px;
  text-align: center;
}

.login-header {
  margin-bottom: 40px;
}

.logo-circle {
  width: 56px;
  height: 56px;
  background: var(--p-text);
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 24px;
  margin: 0 auto 16px;
}

.logo-title {
  font-size: 28px;
  margin-bottom: 4px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  text-align: left;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.full-width {
  width: 100%;
  padding: 16px;
}

.error-box {
  background: #FFF1F0;
  color: #FF3B30;
  padding: 14px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
}

.login-footer {
  text-align: center;
}

.t-tiny {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.opacity-50 { opacity: 0.5; }
</style>
