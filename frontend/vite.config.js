import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    base: '/m/',
    plugins: [vue()],
    server: {
        port: 3000,
        host: true,
    }
})
