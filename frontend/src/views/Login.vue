<template>
  <div class="login-page">
    <!-- Background Decor -->
    <div class="decor blob-1"></div>
    <div class="decor blob-2"></div>

    <div class="login-container animate-fade">
      <div class="login-card">
        <div class="login-header">
          <div class="logo-circle">
            <span>C</span>
          </div>
          <h1 class="logo-title">CanteenPay</h1>
          <p class="logo-subtitle">Система управления финансами</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label class="form-label">Логин</label>
            <input 
              v-model="username"
              type="text" 
              class="input"
              placeholder="admin"
              required
            />
          </div>
          <div class="form-group">
            <label class="form-label">Пароль</label>
            <input 
              v-model="password"
              type="password" 
              class="input"
              placeholder="••••••••"
              required
            />
          </div>

          <button 
            :disabled="loading"
            class="btn btn-primary btn-full"
          >
            {{ loading ? 'Авторизация...' : 'Войти в систему' }}
          </button>
        </form>
        
        <div v-if="error" class="error-box">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

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
    error.value = 'Неверный логин или пароль'
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
  background-color: var(--bg);
  position: relative;
  overflow: hidden;
  padding: 1.5rem;
}

.decor {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  z-index: 0;
}

.blob-1 {
  top: -100px;
  left: -100px;
  width: 500px;
  height: 500px;
  background: var(--primary);
}

.blob-2 {
  bottom: -100px;
  right: -100px;
  width: 500px;
  height: 500px;
  background: var(--accent);
}

.login-container {
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 2;
}

.login-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  padding: 3rem;
  border-radius: 40px;
  border: 1px solid var(--surface);
  box-shadow: var(--shadow-lg);
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-circle {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  font-size: 1.8rem;
  margin: 0 auto 1.5rem;
  box-shadow: 0 10px 20px rgba(0, 102, 255, 0.2);
}

.logo-title {
  font-size: 2rem;
  color: var(--text);
  margin-bottom: 0.25rem;
}

.logo-subtitle {
  color: var(--text-soft);
  font-weight: 500;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 10px;
  font-weight: 800;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  padding-left: 0.5rem;
}

.btn-full {
  width: 100%;
  padding: 1.1rem;
  margin-top: 1rem;
  font-size: 1rem;
  background: var(--text);
}

.btn-full:hover {
  background: #000;
  transform: translateY(-2px);
}

.error-box {
  margin-top: 1.5rem;
  background: #fff1f2;
  color: #e11d48;
  padding: 1rem;
  border-radius: var(--radius);
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  border: 1px solid #ffe4e6;
}
</style>
