// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/ui'],

  runtimeConfig: {
      public: {
          apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000',
      },
  },

  ui: {
      icons: ['heroicons'],
  },

  compatibilityDate: '2025-03-03',
});