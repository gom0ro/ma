import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token') || null,
    }),
    actions: {
        async login(username, password) {
            const params = new URLSearchParams()
            params.append('username', username)
            params.append('password', password)

            const { data } = await api.post('/auth/login', params)
            this.token = data.access_token
            localStorage.setItem('token', this.token)
            await this.fetchUser()
        },
        async fetchUser() {
            if (!this.token) return
            try {
                const { data } = await api.get('/auth/me')
                this.user = data
            } catch (e) {
                this.logout()
            }
        },
        logout() {
            this.user = null
            this.token = null
            localStorage.removeItem('token')
        }
    }
})
