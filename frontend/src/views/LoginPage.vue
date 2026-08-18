<template>
  <div class="auth-page">
    <div class="auth-side">
      <router-link to="/" class="logo">AIWise</router-link>
      <div class="auth-side-content">
        <blockquote>"Knowledge is power."</blockquote>
        <cite>— Sir Francis Bacon</cite>
      </div>
    </div>

    <div class="auth-main">
      <div class="auth-box">
        <h1>Welcome back</h1>
        <p class="auth-sub">Log in to continue your learning streak.</p>

        <form @submit.prevent="handleLogin" class="auth-form" novalidate>
          <div class="field" :class="{ 'field--error': errors.email }">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="you@example.com"
              autocomplete="email"
            />
            <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
          </div>

          <div class="field" :class="{ 'field--error': errors.password }">
            <label for="password">Password</label>
            <div class="input-wrap">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                autocomplete="current-password"
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
          </div>

          <div class="forgot-row">
            <router-link to="/forgot-password" class="forgot-link">Forgot password?</router-link>
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Log in</span>
          </button>

          <p v-if="serverError" class="server-error">{{ serverError }}</p>
        </form>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register">Create one</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useReCaptcha } from 'vue-recaptcha-v3'
import api from '../services/api'

const router = useRouter()
const recaptcha = useReCaptcha()
const showPassword = ref(false)
const loading = ref(false)
const serverError = ref('')

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })

function validate() {
  errors.email = ''
  errors.password = ''
  let valid = true
  if (!form.email) { errors.email = 'Email is required.'; valid = false }
  else if (!/\S+@\S+\.\S+/.test(form.email)) { errors.email = 'Enter a valid email.'; valid = false }
  if (!form.password) { errors.password = 'Password is required.'; valid = false }
  return valid
}

async function handleLogin() {
  if (!validate()) return
  loading.value = true
  serverError.value = ''
  try {
    let token = ''

    if (recaptcha) {
      try {
        await recaptcha.recaptchaLoaded()
        token = await recaptcha.executeRecaptcha('login')
      } catch (recaptchaError) {
        console.warn('reCAPTCHA could not create a token:', recaptchaError)
      }
    }

    const response = await api.post('/login', {
      email: form.email,
      password: form.password,
      recaptchaToken: token
    })

    console.log(response.data)
    router.push('/dashboard')

  } catch (e) {
    if (e.response?.status === 429) {
      serverError.value = 'Too many login attempts. Please wait a minute and try again.'
    } else {
      serverError.value = e.response?.data?.message || 'Unable to connect to the server.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: grid;
  grid-template-columns: 420px 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Side panel */
.auth-side {
  background: #3730a3;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.logo { font-weight: 800; font-size: 22px; color: #fff; text-decoration: none; }
.auth-side-content { padding-bottom: 48px; }
blockquote { font-size: 22px; font-weight: 600; color: #fff; line-height: 1.5; margin: 0 0 12px; font-style: italic; }
cite { font-size: 13px; color: #a5b4fc; font-style: normal; }

/* Main */
.auth-main {
  background: #fafaf8;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.auth-box { width: 100%; max-width: 400px; }
.auth-box h1 { font-size: 30px; font-weight: 800; letter-spacing: -0.5px; margin: 0 0 8px; color: #0f0f0f; }
.auth-sub { color: #666; font-size: 15px; margin: 0 0 36px; }

/* Form */
.auth-form { display: flex; flex-direction: column; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 14px; font-weight: 600; color: #222; }
.field input {
  height: 44px;
  padding: 0 14px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  background: #fff;
  outline: none;
  transition: border-color 0.15s;
  width: 100%;
  box-sizing: border-box;
}
.field input:focus { border-color: #3730a3; }
.field--error input { border-color: #dc2626; }
.field-error { font-size: 13px; color: #dc2626; }

.input-wrap { position: relative; }
.input-wrap input { padding-right: 60px; }
.toggle-pw {
  position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
  background: none; border: none; font-size: 13px; color: #6b7280; cursor: pointer; font-weight: 600;
}

.forgot-row { text-align: right; margin-top: -8px; }
.forgot-link { font-size: 13px; color: #3730a3; text-decoration: none; }
.forgot-link:hover { text-decoration: underline; }

.btn-submit {
  height: 46px;
  background: #3730a3;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.btn-submit:hover:not(:disabled) { background: #312e81; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.server-error { font-size: 13px; color: #dc2626; text-align: center; margin: 0; }

.auth-footer { text-align: center; font-size: 14px; color: #666; margin-top: 32px; }
.auth-footer a { color: #3730a3; font-weight: 600; text-decoration: none; }
.auth-footer a:hover { text-decoration: underline; }

@media (max-width: 900px) {
  .auth-page { grid-template-columns: 1fr; }
  .auth-side { display: none; }
}
</style>
