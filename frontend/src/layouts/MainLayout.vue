<template>
  <div class="app-shell">
    <!-- Sidebar -->
    <aside :class="['sidebar', { 'is-mobile-open': isMenuOpen }]">
      <div class="brand">
        <div class="brand-logo">C</div>
        <div class="brand-name">CanteenPay</div>
      </div>
      
      <nav class="nav">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path"
          class="nav-item"
          active-class="active"
          @click="isMenuOpen = false"
        >
          <component :is="item.icon" class="nav-icon" />
          <span>{{ item.name }}</span>
        </router-link>
      </nav>

      <div class="sidebar-user">
        <div class="user-meta">
          <p class="user-name">{{ authStore.user?.full_name || 'Admin' }}</p>
          <p class="t-small">Администратор</p>
        </div>
        <button @click="logout" class="logout-btn">
          <LogOut size="18" />
        </button>
      </div>
    </aside>

    <!-- Mobile Header -->
    <header class="mobile-nav">
      <div class="brand-sm">C</div>
      <button @click="isMenuOpen = !isMenuOpen" class="menu-btn">
        <Menu v-if="!isMenuOpen" />
        <X v-else />
      </button>
    </header>

    <!-- Main -->
    <main class="main">
      <div class="content-wrapper animate-view">
        <header class="content-header">
          <div>
            <h1 class="page-title">{{ currentRouteName }}</h1>
            <p class="t-small">{{ formattedDate }}</p>
          </div>
        </header>
        <router-view></router-view>
      </div>
    </main>

    <div v-if="isMenuOpen" class="overlay" @click="isMenuOpen = false"></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  LayoutDashboard, 
  Receipt, 
  BarChart3, 
  Wallet, 
  Replace, 
  Calendar as CalendarIcon,
  LogOut,
  Menu,
  X
} from 'lucide-vue-next'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isMenuOpen = ref(false)

const formattedDate = new Date().toLocaleDateString('ru-RU', { 
  year: 'numeric', month: 'long', day: 'numeric' 
})

const navItems = [
  { name: 'Дашборд', path: '/', icon: LayoutDashboard },
  { name: 'Расходы', path: '/expenses', icon: Receipt },
  { name: 'Финансы', path: '/finances', icon: BarChart3 },
  { name: 'Касса', path: '/cashier', icon: Wallet },
  { name: 'Сравнение', path: '/compare', icon: Replace },
  { name: 'Календарь', path: '/calendar', icon: CalendarIcon },
]

const currentRouteName = computed(() => {
  return navItems.find(item => item.path === route.path)?.name || 'Обзор'
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  background: white;
  border-right: 1px solid var(--p-border);
  display: flex;
  flex-direction: column;
  padding: 40px 24px;
  position: sticky;
  top: 0;
  height: 100vh;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 48px;
  padding-left: 12px;
}

.brand-logo {
  width: 32px;
  height: 32px;
  background: var(--p-text);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}

.brand-name {
  font-weight: 800;
  font-size: 18px;
  letter-spacing: -0.04em;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  color: var(--p-text-sec);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: var(--p-transition);
}

.nav-item:hover {
  background: #F5F5F7;
  color: var(--p-text);
}

.nav-item.active {
  background: #F2F2F7;
  color: var(--p-text);
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.sidebar-user {
  margin-top: 40px;
  padding: 20px;
  background: #F5F5F7;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
}

.logout-btn {
  background: none;
  border: none;
  color: var(--p-text-sec);
  cursor: pointer;
  padding: 4px;
  transition: var(--p-transition);
}

.logout-btn:hover { color: var(--p-error); }

.mobile-nav {
  display: none;
  height: 64px;
  background: white;
  border-bottom: 1px solid var(--p-border);
  padding: 0 20px;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 50;
}

.brand-sm {
  width: 32px;
  height: 32px;
  background: var(--p-text);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}

.menu-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
}

.content-header {
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  margin-bottom: 4px;
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.2);
  backdrop-filter: blur(4px);
  z-index: 40;
}

@media (max-width: 1024px) {
  .sidebar {
    position: fixed;
    left: -280px;
    top: 0;
    bottom: 0;
    z-index: 100;
    width: 280px;
    transition: left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .sidebar.is-mobile-open { left: 0; }
  .mobile-nav { display: flex; }
}
</style>
