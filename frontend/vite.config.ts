import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // The backend project owns the .env file, so Vite explicitly reads those values too.
  const frontendEnv = loadEnv(mode, process.cwd(), '')
  const rootEnv = loadEnv(mode, fileURLToPath(new URL('..', import.meta.url)), '')
  const backendEnv = loadEnv(mode, fileURLToPath(new URL('../backend', import.meta.url)), '')
  const backendSrcEnv = loadEnv(mode, fileURLToPath(new URL('../backend/src', import.meta.url)), '')
  const recaptchaSiteKey =
    // Prefer frontend-specific keys, then fall back to root/backend env files.
    frontendEnv.RECAPTCHA_SITE_KEY ||
    frontendEnv.VITE_RECAPTCHA_SITE_KEY ||
    rootEnv.RECAPTCHA_SITE_KEY ||
    rootEnv.VITE_RECAPTCHA_SITE_KEY ||
    backendEnv.RECAPTCHA_SITE_KEY ||
    backendEnv.VITE_RECAPTCHA_SITE_KEY ||
    backendSrcEnv.RECAPTCHA_SITE_KEY ||
    backendSrcEnv.VITE_RECAPTCHA_SITE_KEY ||
    ''

  return {
    plugins: [
      vue(),
      vueDevTools(),
    ],
    define: {
      'import.meta.env.RECAPTCHA_SITE_KEY': JSON.stringify(recaptchaSiteKey),
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
