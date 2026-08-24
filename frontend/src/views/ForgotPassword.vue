<template>
  <div class="auth-page">
    <div class="auth-side">
      <router-link to="/" class="logo">AIWise</router-link>
      <div class="auth-side-content">
        <div class="perks">
          <div class="perk" v-for="perk in perks" :key="perk.title">
            <span class="perk-icon">{{ perk.icon }}</span>
            <div>
              <strong>{{ perk.title }}</strong>
              <p>{{ perk.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="auth-main">
      <div class="auth-box">
        <h1>Forgot your password?</h1>
        <p class="auth-sub">No problem! Enter a new password.</p>

        <form @submit.prevent="handleReset" class="auth-form" novalidate>
          <div class="field" :class="{ 'field--error': errors.email }">
            <label for="email">Email</label>
            <input id="email" v-model="form.email" type="email" placeholder="you@example.com" autocomplete="email" />
            <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
          </div>

          <div class="field" :class="{ 'field--error': errors.oldPassword }">
            <label for="password"> Old Password</label>
            <div class="input-wrap">
              <input
                id="oldPassword"
                v-model="form.oldPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="At least 8 characters"
                autocomplete="new-password"
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div class="pw-strength" v-if="form.oldPassword">
              <div class="pw-bar" :class="`pw-bar--${pwStrength.level}`">
                <div class="pw-fill" :style="{ width: pwStrength.pct + '%' }"></div>
              </div>
              <span class="pw-label">{{ pwStrength.label }}</span>
            </div>
            <span v-if="errors.oldPassword" class="field-error">{{ errors.oldPassword }}</span>
          </div>

          <div class="field" :class="{ 'field--error': errors.newPassword }">
            <label for="password"> New Password</label>
            <div class="input-wrap">
              <input
                id="newPassword"
                v-model="form.newPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="At least 8 characters"
                autocomplete="new-password"
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div class="pw-strength" v-if="form.newPassword">
              <div class="pw-bar" :class="`pw-bar--${pwStrength.level}`">
                <div class="pw-fill" :style="{ width: pwStrength.pct + '%' }"></div>
              </div>
              <span class="pw-label">{{ pwStrength.label }}</span>
            </div>
            <span v-if="errors.newPassword" class="field-error">{{ errors.newPassword }}</span>
          </div>

          <div class="field" :class="{ 'field--error': errors.confirmPassword }">
            <label for="password"> Confirm Password</label>
            <div class="input-wrap">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                placeholder="At least 8 characters"
                autocomplete="new-password"
              />
              <button type="button" class="toggle-pw" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
            <div class="pw-strength" v-if="form.confirmPassword">
              <div class="pw-bar" :class="`pw-bar--${pwStrength.level}`">
                <div class="pw-fill" :style="{ width: pwStrength.pct + '%' }"></div>
              </div>
              <span class="pw-label">{{ pwStrength.label }}</span>
            </div>
            <span v-if="errors.confirmPassword" class="field-error">{{ errors.confirmPassword }}</span>
          </div>

          <button type="submit" class="btn-submit" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            <span v-else>Reset Password</span>
          </button>

          <p class="terms">
            By signing up, you agree to our
            <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
          </p>

          <p v-if="serverError" class="server-error">{{ serverError }}</p>
        </form>

        <p class="auth-footer">
          Already have an account?
          <router-link to="/login">Log in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useReCaptcha } from 'vue-recaptcha-v3'
import { useRouter } from 'vue-router'

import api from '../services/api'
const router = useRouter()
const showPassword = ref(false)
const recaptcha = useReCaptcha()
const loading = ref(false)
const serverError = ref('')

const perks = [
  { icon: '📚', title: 'Curated article library', desc: 'Thousands of articles across dozens of topics.' },
  { icon: '🧠', title: 'Adaptive quizzes', desc: 'Questions that adjust to your knowledge level.' },
  { icon: '📈', title: 'Progress tracking', desc: 'See retention improve week over week.' },
]

const form = reactive({ email: '', oldPassword: '', newPassword: '', confirmPassword: '' })
const errors = reactive({ email: '', oldPassword: '', newPassword: '', confirmPassword: '' })

// Mirror the password rules visually so users can fix weak passwords before submitting.
const pwStrength = computed(() => {
  const p = form.newPassword
  if (!p) return { level: 'none', pct: 0, label: '' }
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  if (p.length >= 12) score++
  const levels = ['weak', 'weak', 'fair', 'good', 'strong']
  const labels = ['Weak', 'Weak', 'Fair', 'Good', 'Strong']
  return { level: levels[score], pct: (score / 4) * 100, label: labels[score] }
})

function validate() {
  // Keep validation on the page so the backend only receives complete reset requests.
  let valid = true

  Object.keys(errors).forEach(k => errors[k] = '')

  if (!form.email) {
    errors.email = 'Email is required.'
    valid = false
  } else if (!/\S+@\S+\.\S+/.test(form.email)) {
    errors.email = 'Enter a valid email.'
    valid = false
  }

  if (!form.oldPassword) {
    errors.oldPassword = 'Password is required.'
    valid = false
  }

  if (!form.newPassword) {
    errors.newPassword = 'Password is required.'
    valid = false
  } else if (form.newPassword.length < 8) {
    errors.newPassword = 'Must be at least 8 characters.'
    valid = false
  } else if (form.newPassword.length > 28) {
    errors.newPassword = 'Must be less than 28 characters.'
    valid = false
  } else if (
    !/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*()]).{8,28}/.test(form.newPassword)
  ) {
    errors.newPassword =
      'Must contain uppercase, lowercase, number and special character.'
    valid = false
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Password is required.'
    valid = false
  } else if (form.confirmPassword.length < 8) {
    errors.confirmPassword = 'Must be at least 8 characters.'
    valid = false
  } else if (form.confirmPassword.length > 28) {
    errors.confirmPassword = 'Must be less than 28 characters.'
    valid = false
  } else if (
    !/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*()]).{8,28}/.test(form.confirmPassword)
  ) {
    errors.confirmPassword =
      'Must contain uppercase, lowercase, number and special character.'
    valid = false
  }

  if (form.newPassword !== form.confirmPassword) {
    errors.confirmPassword = "Passwords do not match."
    valid = false
  }

  return valid
}

async function handleReset() {
  if (!validate()) return
  loading.value = true
  serverError.value = ''
  try {
    let token = ''

    if (recaptcha) {
      try {
        // reCAPTCHA v3 is invisible; it creates a token instead of showing a checkbox popup.
        await recaptcha.recaptchaLoaded()
        token = await recaptcha.executeRecaptcha('change_password')
      } catch (recaptchaError) {
        console.warn('reCAPTCHA could not create a token:', recaptchaError)
      }
    }

    // Send both the old and new passwords so the backend can confirm ownership.
    const response = await api.post('/changePassword', {
      email: form.email,
      oldPassword: form.oldPassword,
      newPassword: form.newPassword,
      confirmPassword: form.confirmPassword,
      recaptchaToken: token
    })
    console.log(response.data)

    // Clear the form after a successful password change.
    form.email = ''
    form.oldPassword = ''
    form.newPassword = ''
    form.confirmPassword = ''

    router.push('/login')

  } catch (e) {
    // Prefer the backend message, then fall back to a connection-style error.
    console.log(e)
    if (e.response) {
      serverError.value = e.response.data.message
    } else {
      serverError.value = 'Unable to connect to the server.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: grid;
  grid-template-columns: 380px 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
}
.auth-side {
  background: #3730a3;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.logo { font-weight: 800; font-size: 22px; color: #fff; text-decoration: none; }
.auth-side-content { padding-bottom: 48px; }

.perks { display: flex; flex-direction: column; gap: 28px; }
.perk { display: flex; gap: 16px; align-items: flex-start; }
.perk-icon { font-size: 22px; line-height: 1; margin-top: 2px; }
.perk strong { display: block; color: #fff; font-size: 15px; margin-bottom: 4px; }
.perk p { color: #a5b4fc; font-size: 13px; margin: 0; line-height: 1.5; }

.auth-main {
  background: #fafaf8;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.auth-box { width: 100%; max-width: 440px; }
.auth-box h1 { font-size: 28px; font-weight: 800; letter-spacing: -0.5px; margin: 0 0 8px; color: #0f0f0f; }
.auth-sub { color: #666; font-size: 15px; margin: 0 0 32px; }

.auth-form { display: flex; flex-direction: column; gap: 20px; }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 14px; font-weight: 600; color: #222; }
.field input {
  height: 44px; padding: 0 14px;
  border: 1.5px solid #d1d5db; border-radius: 8px;
  font-size: 15px; background: #fff; outline: none;
  transition: border-color 0.15s; width: 100%; box-sizing: border-box;
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

.pw-strength { display: flex; align-items: center; gap: 10px; }
.pw-bar { height: 4px; flex: 1; background: #e5e7eb; border-radius: 2px; overflow: hidden; }
.pw-fill { height: 100%; border-radius: 2px; transition: width 0.3s; background: #dc2626; }
.pw-bar--fair .pw-fill { background: #f59e0b; }
.pw-bar--good .pw-fill { background: #10b981; }
.pw-bar--strong .pw-fill { background: #3730a3; }
.pw-label { font-size: 12px; color: #888; width: 44px; }

.btn-submit {
  height: 46px; background: #3730a3; color: #fff; border: none;
  border-radius: 8px; font-size: 15px; font-weight: 700; cursor: pointer;
  transition: background 0.15s; display: flex; align-items: center; justify-content: center;
}
.btn-submit:hover:not(:disabled) { background: #312e81; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.4); border-top-color: #fff;
  border-radius: 50%; animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.terms { font-size: 12px; color: #9ca3af; text-align: center; margin: 0; }
.terms a { color: #6366f1; }

.server-error { font-size: 13px; color: #dc2626; text-align: center; margin: 0; }

.auth-footer { text-align: center; font-size: 14px; color: #666; margin-top: 28px; }
.auth-footer a { color: #3730a3; font-weight: 600; text-decoration: none; }
.auth-footer a:hover { text-decoration: underline; }

@media (max-width: 900px) {
  .auth-page { grid-template-columns: 1fr; }
  .auth-side { display: none; }
  .field-row { grid-template-columns: 1fr; }
}
</style>
