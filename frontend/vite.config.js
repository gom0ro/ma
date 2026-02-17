import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    base: '/ma/',
    plugins: [vue()],
    server: {
        port: 3000,
        host: true,
    }
})
