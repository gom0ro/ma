import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'https://ma-kuz4.onrender.com',
    timeout: 10000, // 10 seconds timeout
})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log('API Request:', config.method.toUpperCase(), config.url, 'Token:', token.substring(0, 10) + '...')
    } else {
        console.log('API Request:', config.method.toUpperCase(), config.url, 'No token found')
    }
    return config
})

export default api
