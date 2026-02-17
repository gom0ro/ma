import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Expenses from '../views/Expenses.vue'
import Finances from '../views/Finances.vue'
import Cashier from '../views/Cashier.vue'
import Compare from '../views/Compare.vue'
import Login from '../views/Login.vue'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/',
        component: MainLayout,
        children: [
            { path: '', name: 'Dashboard', component: Dashboard },
            { path: 'expenses', name: 'Expenses', component: Expenses },
            { path: 'finances', name: 'Finances', component: Finances },
            { path: 'cashier', name: 'Cashier', component: Cashier },
            { path: 'compare', name: 'Compare', component: Compare },
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.name !== 'Login' && !token) {
        next({ name: 'Login' })
    } else {
        next()
    }
})

export default router
