import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';

const apiProxyTarget = process.env.VITE_API_PROXY_TARGET ?? 'http://localhost:80';

export default defineConfig({
  plugins: [
    vue(),
    vuetify({ autoImport: true }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: apiProxyTarget,
        changeOrigin: true,
      },
    },
  },
  build: {
    chunkSizeWarningLimit: 700,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/vuetify')) {
            return 'vuetify';
          }

          if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router')) {
            return 'vue-core';
          }

          if (id.includes('/src/features/auth/')) {
            return 'feature-auth';
          }

          if (id.includes('/src/features/tools/')) {
            return 'feature-tools';
          }

          if (id.includes('/src/features/profile/')) {
            return 'feature-profile';
          }

          return undefined;
        },
      },
    },
  },
});
