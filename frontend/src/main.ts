import './assets/main.css'

import { createApp } from 'vue'
import { VueReCaptcha } from 'vue-recaptcha-v3'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)

const recaptchaSiteKey = import.meta.env.RECAPTCHA_SITE_KEY

if (recaptchaSiteKey) {
  app.use(VueReCaptcha, {
    siteKey: recaptchaSiteKey,
    loaderOptions: {}
  })
} else {
  console.warn('reCAPTCHA site key is not configured. Login will rely on the backend development fallback.')
}

app.mount('#app')
