// Configuration file for Vite, the build tool for the Annonaria frontend.
// Defines plugins, path aliases, and server settings for the Vue.js application,
// optimized for development and Dockerized deployment.

import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true,       // listen on 0.0.0.0
    port: 5173,       // default port, mapped in docker-compose
    strictPort: true  // avoid random fallback ports
  }
})
