<template>
  <div class="page-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <router-link to="/" class="logo">AIWise</router-link>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">⊞</span> Dashboard
        </router-link>
        <router-link to="/articles" class="nav-item">
          <span class="nav-icon">◫</span> Articles
        </router-link>
        <router-link to="/account" class="nav-item nav-item--active">
          <span class="nav-icon">◯</span> Account
        </router-link>
      </nav>
      <div class="sidebar-bottom">
        <div class="user-card">
          <div class="avatar">AR</div>
          <div>
            <div class="user-name">Tyler Durden</div>
            <div class="user-email">tyler@PaperStreetSoapCo.com</div>
          </div>
        </div>
        <button class="logout-btn" type="button" @click="handleLogout">Log out</button>
      </div>
    </aside>

    <main class="main">
      <header class="page-header">
        <h1>Account</h1>
        <p class="header-sub">Manage your profile and preferences.</p>
      </header>

      <div class="account-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          class="tab-btn"
          :class="{ 'tab-btn--active': activeTab === tab.key }"
          @click="activeTab = tab.key"
        >{{ tab.label }}</button>
      </div>

      <!-- Profile -->
      <section v-if="activeTab === 'profile'" class="card">
        <div class="card-section">
          <h2>Profile information</h2>
          <h3>Please complete all fields to update profile details.</h3>
          <div style="height: 20px;"></div>
          <form @submit.prevent="handleUpdateAccount" class="form-grid">
            <div class="field">
              <label>First name</label>
              <input v-model="updateForm.firstName" type="text" />
            </div>
            <div class="field">
              <label>Last name</label>
              <input v-model="updateForm.lastName" type="text" />
            </div>
            <div class="field field--full">
              <label>Email</label>
              <input v-model="updateForm.email" type="email" />
            </div>
            <div class="field field--full">
              <label>Bio <span class="optional">(optional)</span></label>
              <textarea v-model="updateForm.bio" rows="3" placeholder="Tell us a bit about yourself…"></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">Save changes</button>
              <span v-if="profileSaved" class="saved-msg">✓ Saved</span>
            </div>
          </form>
        </div>
      </section>

      <!-- Password -->
      <section v-if="activeTab === 'password'" class="card">
        <div class="card-section">
          <h2>Need to update your password? No worries, click the button below.</h2>
            <router-link to="/forgot-password" class="btn-reset-password">
                Change Password
            </router-link>
        </div>
      </section>

      <!-- Email Preferences -->
      <section v-if="activeTab === 'email verification'" class="card">
        <div class="card-section">
        <div>
            <button class="btn-verfi" >Verify Email</button>
            <div class="danger-desc">Email verification for accounts is a security process that ensures a user controls the email address they register with.</div>
        </div>
          <div class="prefs-list">
            <div class="pref-row" v-for="pref in prefs" :key="pref.key">
              <div class="pref-info">
                <div class="pref-label">{{ pref.label }}</div>
                <div class="pref-desc">{{ pref.desc }}</div>
              </div>
              <button
                class="toggle"
                :class="{ 'toggle--on': pref.value }"
                @click="pref.value = !pref.value"
                :aria-pressed="pref.value"
              >
                <span class="toggle-thumb"></span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Danger zone -->
      <section v-if="activeTab === 'danger'" class="card card--danger">
        <div class="card-section">
          <h2>Danger zone</h2>
          <div class="danger-row">
            <div>
              <div class="danger-label">Delete account</div>
              <div class="danger-desc">Permanently remove your account and all associated data. This cannot be undone.</div>
            </div>
            <button class="btn-danger" @click="confirmDelete = true">Delete account</button>
          </div>
        </div>
      </section>

      <!-- Delete confirmation modal -->
      <div class="modal-backdrop" v-if="confirmDelete" @click.self="confirmDelete = false">
       <div class="modal">
        <h2>Delete Account</h2>

        <p>
            Enter your email to permanently delete your account.
        </p>

        <form @submit.prevent="handleDeleteAccount">

          <div class="field">
            <label>Email</label>
            <input
              v-model="deleteForm.email"
              type="email"
              required
            />
          </div>

          <div style="height: 20px;"></div>

          <div class="modal-actions">
            <button
              type="button"
              class="btn-outline"
              @click="confirmDelete = false"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="btn-danger"
            >
              Delete Account
            </button>
          </div>

          <p v-if="serverError" class="field-error">
            {{ serverError }}
          </p>

        </form>
    </div>
    </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'


const router = useRouter()
const activeTab = ref('profile')
const profileSaved = ref(false)
const confirmDelete = ref(false)
const loading = ref(false)
const serverError = ref('')

const deleteForm = reactive({ email: ''})
const updateForm = reactive({ firstName: '', lastName: '', email: '', bio: ''})
const errors = reactive({  email: '' })


const tabs = [
  { key: 'profile', label: 'Profile' },
  { key: 'password', label: 'Password' },
  { key: 'email verification', label: 'Email verification' },
  { key: 'danger', label: 'Danger zone' },
]

const profile = reactive({
  firstName: 'Alex',
  lastName: 'Rivera',
  email: 'alex@example.com',
  bio: '',
})

const pw = reactive({ current: '', next: '', confirm: '' })

const prefs = reactive([
  { key: 'quizReminders', label: 'Quiz reminders', desc: 'Get notified when you have uncompleted quizzes.', value: false },
  { key: '2StepVerification', label: 'Enable  2-Step Verification', desc: "Add an extra layer of security by requiring a password and security question", value: true }
])

function saveProfile() {
  profileSaved.value = true
  setTimeout(() => { profileSaved.value = false }, 3000)
}

function validateUpdate() {
  let valid = true

  Object.keys(errors).forEach(k => errors[k] = '')

  if (!updateForm.email) {
    serverError.value = 'Email is required.'
    valid = false
  } else if (!/\S+@\S+\.\S+/.test(updateForm.email)) {
    errors.email = 'Enter a valid email.'
    valid = false
  }
  if (!updateForm.firstName) {
    errors.firstName = 'Required.'
    valid = false
  }

  if (!updateForm.lastName) {
    errors.lastName = 'Required.'
    valid = false
  }

  if (!updateForm.lastName) {
    errors.lastName = 'Required.'
    valid = false
  }

  return valid
}

function validateEmail() {
  let valid = true

  Object.keys(errors).forEach(k => errors[k] = '')

  if (!deleteForm.email) {
    errors.email = 'Email is required.'
    valid = false
  } else if (!/\S+@\S+\.\S+/.test(deleteForm.email)) {
    errors.email = 'Enter a valid email.'
    valid = false
  }

  return valid
}

async function handleLogout() {
  try {
  await api.post("/logout")

    localStorage.clear()
    sessionStorage.clear()

    router.push("/")
  } catch (e) {
    console.error("Logout failed:", e)
  }
}

async function handleDeleteAccount() {
  console.log("Delete function called");
  if (!validateEmail()) return
  loading.value = true
  serverError.value = ''
  try {
    const response = await api.post('/deleteAccount', {
    })
    console.log(response.data)

    // Clear the form
    deleteForm.email = ''

    router.push('/login')

  } catch (e) {
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

async function handleUpdateAccount() {
  if (!validateUpdate()) return
  loading.value = true
  serverError.value = ''
  try {
    const response = await api.post('/updateAccount', {
      firstName: updateForm.firstName,
      lastName: updateForm.lastName,
      bio: updateForm.bio
    })
    console.log(response.data)

    // Clear the form
    updateForm.firstName = ''
    updateForm.lastName = ''
    updateForm.email = ''
    updateForm.bio = ''

    profileSaved.value = true

    setTimeout(() => {
        profileSaved.value = false
    }, 3000)

  } catch (e) {
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
.page-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  background: #f5f5f0;
}

.sidebar {
  background: #1e1b4b; display: flex; flex-direction: column;
  position: sticky; top: 0; height: 100vh;
}
.sidebar-logo { padding: 28px 24px 20px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.logo { font-weight: 800; font-size: 20px; color: #fff; text-decoration: none; }
.sidebar-nav { flex: 1; padding: 16px 12px; display: flex; flex-direction: column; gap: 4px; }
.nav-item {
  display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px;
  font-size: 14px; font-weight: 500; color: #a5b4fc; text-decoration: none; transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.07); color: #fff; }
.nav-item--active { background: rgba(255,255,255,0.12); color: #fff; }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }
.sidebar-bottom { padding: 16px 12px; border-top: 1px solid rgba(255,255,255,0.08); }
.user-card { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 36px; height: 36px; background: #3730a3; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.user-name { font-size: 13px; font-weight: 600; color: #fff; }
.user-email { font-size: 11px; color: #818cf8; }
.logout-btn {
  width: 100%;
  margin-top: 16px;
  padding: 10px 12px;
  border: 1px solid rgba(255,255,255,0.16);
  border-radius: 8px;
  background: rgba(255,255,255,0.08);
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.logout-btn:hover {
  background: rgba(255,255,255,0.14);
  border-color: rgba(255,255,255,0.28);
}

.main { padding: 40px; max-width: 720px; }
.page-header { margin-bottom: 28px; }
.page-header h1 { font-size: 26px; font-weight: 800; margin: 0 0 4px; color: #0f0f0f; }
.header-sub { font-size: 14px; color: #666; margin: 0; }

.account-tabs { display: flex; gap: 4px; margin-bottom: 24px; border-bottom: 1px solid #e5e5e5; padding-bottom: 0; }
.tab-btn {
  padding: 10px 18px; background: none; border: none; border-bottom: 2px solid transparent;
  font-size: 14px; font-weight: 500; color: #888; cursor: pointer; transition: all 0.15s;
  margin-bottom: -1px;
}
.tab-btn:hover { color: #3730a3; }
.tab-btn--active { color: #3730a3; border-bottom-color: #3730a3; font-weight: 600; }

.card { background: #fff; border-radius: 12px; border: 1px solid #e5e5e5; overflow: hidden; }
.card--danger { border-color: #fecaca; }
.card-section { padding: 28px; }
.card-section h2 { font-size: 16px; font-weight: 700; margin: 0 0 24px; color: #0f0f0f; }

.avatar-row { display: flex; align-items: center; gap: 20px; margin-bottom: 28px; }
.avatar-lg {
  width: 64px; height: 64px; background: #3730a3; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; color: #fff; flex-shrink: 0;
}
.hint { font-size: 12px; color: #aaa; margin: 6px 0 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field--full { grid-column: 1 / -1; }
.field label { font-size: 13px; font-weight: 600; color: #444; }
.optional { font-weight: 400; color: #aaa; }
.field input, .field textarea {
  padding: 10px 14px; border: 1.5px solid #d1d5db; border-radius: 8px;
  font-size: 14px; background: #fff; outline: none; transition: border-color 0.15s;
  font-family: inherit; resize: vertical;
}
.field input:focus, .field textarea:focus { border-color: #3730a3; }
.field-error { font-size: 12px; color: #dc2626; }

.form-actions { grid-column: 1 / -1; display: flex; align-items: center; gap: 16px; }
.btn-primary {
  background: #3730a3; color: #fff; border: none; border-radius: 8px;
  padding: 10px 22px; font-size: 14px; font-weight: 700; cursor: pointer; transition: background 0.15s;
}
.btn-primary:hover { background: #312e81; }
.btn-outline {
  background: #fff; color: #444; border: 1.5px solid #d1d5db; border-radius: 8px;
  padding: 10px 22px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.15s;
}
.btn-outline:hover { border-color: #3730a3; color: #3730a3; }
.btn-sm { padding: 7px 16px; font-size: 13px; }
.btn-danger {
  background: #dc2626; color: #fff; border: none; border-radius: 8px;
  padding: 10px 22px; font-size: 14px; font-weight: 700; cursor: pointer; transition: background 0.15s; white-space: nowrap;
}
.btn-danger:hover { background: #b91c1c; }
.saved-msg { font-size: 13px; color: #10b981; font-weight: 600; }
.btn-reset-password {
  display: inline-block;
  padding: 12px 20px;
  background: #3730a3;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
}

.btn-reset-password:hover {
  background: #312e81;
}

/* Preferences */
.prefs-list { display: flex; flex-direction: column; gap: 0; }
.pref-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 0; border-bottom: 1px solid #f3f3f3; gap: 24px;
}
.pref-row:last-child { border-bottom: none; }
.pref-label { font-size: 14px; font-weight: 600; color: #1e1b4b; margin-bottom: 2px; }
.pref-desc { font-size: 13px; color: #888; }

.toggle {
  width: 44px; height: 24px; border-radius: 12px; background: #d1d5db;
  border: none; cursor: pointer; position: relative; transition: background 0.2s; flex-shrink: 0;
  padding: 0;
}
.toggle--on { background: #3730a3; }
.toggle-thumb {
  position: absolute; top: 3px; left: 3px;
  width: 18px; height: 18px; background: #fff; border-radius: 50%;
  transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.toggle--on .toggle-thumb { transform: translateX(20px); }

/* Danger */
.danger-row { display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.danger-label { font-size: 15px; font-weight: 700; color: #dc2626; margin-bottom: 4px; }
.danger-desc { font-size: 13px; color: #666; max-width: 380px; line-height: 1.5; }

/* Modal */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
h3 {
  color: #111827;
}
.modal {
  background: #fff; border-radius: 16px; padding: 36px;
  max-width: 420px; width: 90%;
}
.modal h2 { font-size: 20px; font-weight: 800; margin: 0 0 12px; color: #111827; }
.modal p { font-size: 14px; color: #666; line-height: 1.6; margin: 0 0 28px; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

@media (max-width: 768px) {
  .page-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .main { padding: 24px 16px; }
  .form-grid { grid-template-columns: 1fr; }
  .danger-row { flex-direction: column; align-items: flex-start; }
}
</style>
