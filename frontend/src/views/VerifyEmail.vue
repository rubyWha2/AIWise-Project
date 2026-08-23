<template>
  <div class="verify-page">
    <div class="verify-card">

      <!-- State: waiting for verification -->
      <template v-if="state === 'pending'">
        <div class="icon-wrap icon-wrap--pending">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="2" y="6" width="28" height="20" rx="3" stroke="#3730a3" stroke-width="2"/>
            <path d="M2 10l14 9 14-9" stroke="#3730a3" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <h1>Check your inbox</h1>
        <p class="verify-sub">
          We sent a verification link to
          <strong>{{ maskedEmail }}</strong>.
          Click the link in that email to activate your account.
        </p>

        <div class="steps">
          <div class="step" v-for="(step, i) in steps" :key="i" :class="{ 'step--done': i < currentStep }">
            <div class="step-dot">
              <span v-if="i < currentStep" class="step-check">✓</span>
              <span v-else class="step-num">{{ i + 1 }}</span>
            </div>
            <span class="step-label">{{ step }}</span>
          </div>
        </div>

        <div class="resend-row">
          <p class="resend-note">
            Didn't receive it?
            <template v-if="resendCooldown > 0">
              Resend in {{ resendCooldown }}s
            </template>
            <button v-else class="resend-btn" @click="resend" :disabled="resending">
              {{ resending ? 'Sending…' : 'Resend email' }}
            </button>
          </p>
          <p v-if="resentMsg" class="resent-msg">{{ resentMsg }}</p>
        </div>

        <div class="divider"></div>
        <p class="wrong-email">
          Wrong email address?
          <router-link to="/register" class="link">Change it</router-link>
        </p>
      </template>

      <!-- State: verified! -->
      <template v-if="state === 'verified'">
        <div class="icon-wrap icon-wrap--success">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <circle cx="18" cy="18" r="16" stroke="#10b981" stroke-width="2"/>
            <path d="M11 18l5 5 9-10" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1>Email verified!</h1>
        <p class="verify-sub">Your account is now active. You're ready to start learning.</p>
        <div class="verified-stats">
          <div class="vstat">
            <span class="vstat-num">12k+</span>
            <span class="vstat-lbl">Articles</span>
          </div>
          <div class="vstat">
            <span class="vstat-num">Free</span>
            <span class="vstat-lbl">Forever</span>
          </div>
          <div class="vstat">
            <span class="vstat-num">94%</span>
            <span class="vstat-lbl">Retention</span>
          </div>
        </div>
        <button class="btn-primary btn-full" @click="goToDashboard">Go to dashboard →</button>
      </template>

      <!-- State: expired link -->
      <template v-if="state === 'expired'">
        <div class="icon-wrap icon-wrap--error">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <circle cx="18" cy="18" r="16" stroke="#dc2626" stroke-width="2"/>
            <path d="M18 10v10M18 24v2" stroke="#dc2626" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <h1>Link expired</h1>
        <p class="verify-sub">This verification link has expired or already been used. Request a new one below.</p>
        <button class="btn-primary btn-full" @click="resend">Send a new link</button>
        <router-link to="/login" class="link link--center">Back to log in</router-link>
      </template>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

// Page state
const state = ref('pending')

// User email is optional because verification can still work with just the token.
const email = ref(route.query.email ?? '')

const maskedEmail = computed(() => {
  // Mask the address for reassurance without exposing the full email on screen.
  if (!email.value) return ''

  const [local, domain] = email.value.split('@')

  const visible = local.slice(0, 2)
  const masked = '*'.repeat(Math.max(1, local.length - 2))

  return `${visible}${masked}@${domain}`
})

// Progress steps stay static while currentStep changes with verification state.
const steps = [
  'Account created',
  'Email sent',
  'Email verified',
  'Start learning'
]

const currentStep = computed(() => {
  return state.value === 'verified' ? 4 : 2
})

// Resend state prevents repeated email requests while the cooldown is active.
const resending = ref(false)
const resendCooldown = ref(0)
const resentMsg = ref('')

let cooldownTimer = null

async function resend() {
  // Keep resend requests spaced out so accidental double-clicks do not spam email.
  if (resendCooldown.value > 0) return

  resending.value = true
  resentMsg.value = ''

  try {
    await api.post('/resendVerificationEmail')
    resentMsg.value = 'A new verification email has been sent.'
    resendCooldown.value = 60
    cooldownTimer = setInterval(() => {

      resendCooldown.value--

      if (resendCooldown.value <= 0) {
        clearInterval(cooldownTimer)
        resentMsg.value = ''
      }

    }, 1000)

  } catch (e) {
    resentMsg.value =
      e.response?.data?.message ||
      'Unable to send verification email.'

  } finally {
    resending.value = false

  }
}

// Verify email when the page opens using the token from the route query.
onMounted(async () => {

  const token = route.query.token
  if (!token) {
    state.value = 'expired'
    return
  }

  try {
    await api.post('/verifyEmail', {
      token
    })
    state.value = 'verified'

  } catch (e) {
    console.log(e)
    state.value = 'expired'

  }

})

function goToDashboard() {
  router.push('/account')
}

onUnmounted(() => {
  // Clear the cooldown interval when navigating away from the page.
  if (cooldownTimer) {
    clearInterval(cooldownTimer)
  }
})
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  background: #f5f5f0;
  font-family: 'Inter', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  gap: 20px;
}

.verify-card {
  background: #fff;
  border-radius: 20px;
  border: 1px solid #e5e5e5;
  padding: 48px 44px;
  max-width: 460px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0;
}

/* Icon */
.icon-wrap {
  width: 72px; height: 72px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 24px;
}
.icon-wrap--pending  { background: #eef2ff; }
.icon-wrap--success  { background: #ecfdf5; }
.icon-wrap--error    { background: #fef2f2; }

h1 {
  font-size: 26px; font-weight: 900; color: #1e1b4b;
  letter-spacing: -0.5px; margin: 0 0 12px;
}

.verify-sub {
  font-size: 15px; color: #666; line-height: 1.65;
  margin: 0 0 32px; max-width: 340px;
}

/* Steps */
.steps {
  width: 100%; display: flex; flex-direction: column; gap: 0;
  margin-bottom: 28px; text-align: left;
}
.step {
  display: flex; align-items: center; gap: 14px;
  padding: 11px 0; border-bottom: 1px solid #f3f3f3; color: #bbb;
  transition: color 0.2s;
}
.step:last-child { border-bottom: none; }
.step--done { color: #1e1b4b; }

.step-dot {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  background: #f3f3f5; font-size: 12px; font-weight: 700; color: #bbb;
  transition: background 0.2s, color 0.2s;
}
.step--done .step-dot { background: #3730a3; color: #fff; }
.step-check { font-size: 13px; }
.step-label { font-size: 14px; font-weight: 500; }
.step--done .step-label { font-weight: 600; color: #1e1b4b; }

/* Resend */
.resend-row { width: 100%; margin-bottom: 24px; }
.resend-note { font-size: 13px; color: #888; margin: 0; }
.resend-btn {
  background: none; border: none; color: #3730a3; font-weight: 700;
  font-size: 13px; cursor: pointer; padding: 0; text-decoration: underline;
  text-decoration-color: transparent; transition: text-decoration-color 0.15s;
}
.resend-btn:hover { text-decoration-color: #3730a3; }
.resend-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.resent-msg { font-size: 13px; color: #10b981; font-weight: 600; margin: 6px 0 0; }

.divider { width: 100%; height: 1px; background: #f3f3f3; margin-bottom: 20px; }

.wrong-email { font-size: 13px; color: #888; margin: 0; }

/* Verified state */
.verified-stats {
  display: flex; width: 100%;
  border: 1px solid #e5e5e5; border-radius: 12px; overflow: hidden;
  margin-bottom: 24px;
}
.vstat {
  flex: 1; padding: 16px 10px; text-align: center;
  border-right: 1px solid #e5e5e5;
}
.vstat:last-child { border-right: none; }
.vstat-num { display: block; font-size: 20px; font-weight: 900; color: #3730a3; letter-spacing: -0.5px; }
.vstat-lbl { display: block; font-size: 11px; color: #aaa; margin-top: 2px; }

/* Buttons & links */
.btn-primary {
  background: #3730a3; color: #fff; border: none; border-radius: 10px;
  padding: 14px 28px; font-size: 15px; font-weight: 700; cursor: pointer;
  transition: background 0.15s; display: inline-block;
}
.btn-primary:hover { background: #312e81; }
.btn-full { width: 100%; }

.link { color: #3730a3; font-weight: 600; text-decoration: none; font-size: 13px; }
.link:hover { text-decoration: underline; }
.link--center { display: block; text-align: center; margin-top: 14px; }

/* Demo switcher */
.demo-switcher {
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap; justify-content: center;
}
.demo-label { font-size: 12px; color: #aaa; }
.demo-btn {
  padding: 4px 12px; border-radius: 6px; border: 1px solid #e5e5e5;
  background: #fff; font-size: 12px; font-weight: 500; color: #666; cursor: pointer;
  transition: all 0.15s;
}
.demo-btn--active { background: #3730a3; border-color: #3730a3; color: #fff; font-weight: 700; }

@media (max-width: 480px) {
  .verify-card { padding: 32px 24px; }
}
</style>
