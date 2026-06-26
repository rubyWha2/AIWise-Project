<template>
  <div class="dashboard">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <router-link to="/" class="logo">AIWise</router-link>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item nav-item--active">
          <span class="nav-icon">⊞</span> Dashboard
        </router-link>
        <router-link to="/articles" class="nav-item">
          <span class="nav-icon">◫</span> Articles
        </router-link>
        <router-link to="/account" class="nav-item">
          <span class="nav-icon">◯</span> Account
        </router-link>
      </nav>
      <div class="sidebar-bottom">
        <div class="user-card">
          <div class="avatar">AR</div>
          <div>
            <div class="user-name">Alex Rivera</div>
            <div class="user-email">alex@example.com</div>
          </div>
        </div>
      </div>
    </aside>

    <main class="main">
      <header class="page-header">
        <div>
          <h1>Welcome back!</h1>
          <p class="header-sub">You're on a <strong>7-day streak</strong>. Keep it up!</p>
        </div>
        <router-link to="/articles" class="btn-primary">Start reading →</router-link>
      </header>

      <div class="stats-row">
        <div class="stat-card" v-for="stat in stats" :key="stat.label">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-change" :class="stat.up ? 'up' : 'down'">{{ stat.change }}</div>
        </div>
      </div>

      <div class="content-grid">
        <section class="section">
          <div class="section-head">
            <h2>Recent activity</h2>
          </div>
          <div class="activity-list">
            <div class="activity-item" v-for="item in activity" :key="item.title">
              <div class="activity-dot" :class="`activity-dot--${item.type}`"></div>
              <div class="activity-body">
                <div class="activity-title">{{ item.title }}</div>
                <div class="activity-meta">{{ item.meta }}</div>
              </div>
              <div class="activity-score" v-if="item.score !== null">{{ item.score }}%</div>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="section-head">
            <h2>Suggested for you</h2>
          </div>
          <div class="suggestion-list">
            <div class="suggestion" v-for="s in suggestions" :key="s.title">
              <div class="suggestion-tag">{{ s.tag }}</div>
              <div class="suggestion-title">{{ s.title }}</div>
              <div class="suggestion-meta">{{ s.readTime }} min read</div>
              <router-link to="/articles" class="suggestion-link">Read article →</router-link>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
const stats = [
  { label: 'Quizzes taken', value: '47', change: '+5 this week', up: true },
  { label: 'Avg. score', value: '82%', change: '+4% vs last week', up: true },
  { label: 'Articles read', value: '31', change: '+3 this week', up: true },
  { label: 'Current streak', value: '7d', change: 'Personal best!', up: true },
]

const activity = [
  { type: 'quiz', title: 'Quiz: The Roman Republic', meta: 'Today, 9:14 AM', score: 88 },
  { type: 'read', title: 'Article: Origins of the Silk Road', meta: 'Today, 8:50 AM', score: null },
  { type: 'quiz', title: 'Quiz: Quantum Computing Basics', meta: 'Yesterday, 7:32 PM', score: 74 },
  { type: 'read', title: 'Article: How CRISPR Works', meta: 'Yesterday, 7:00 PM', score: null },
  { type: 'quiz', title: 'Quiz: The French Revolution', meta: '2 days ago', score: 91 },
]

const suggestions = [
  { tag: 'Science', title: 'The Secret Life of Mitochondria', readTime: 6 },
  { tag: 'History', title: 'The Fall of Constantinople', readTime: 9 },
  { tag: 'Technology', title: 'How Large Language Models Work', readTime: 8 },
]
</script>

<style scoped>
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  background: #f5f5f0;
}

/* Sidebar */
.sidebar {
  background: #1e1b4b;
  display: flex;
  flex-direction: column;
  padding: 0;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-logo { padding: 28px 24px 20px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.logo { font-weight: 800; font-size: 20px; color: #fff; text-decoration: none; }
.sidebar-nav { flex: 1; padding: 16px 12px; display: flex; flex-direction: column; gap: 4px; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px; border-radius: 8px;
  font-size: 14px; font-weight: 500; color: #a5b4fc;
  text-decoration: none; transition: background 0.15s, color 0.15s;
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

/* Main */
.main { padding: 40px; overflow-y: auto; }

.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 32px; }
.page-header h1 { font-size: 26px; font-weight: 800; margin: 0 0 4px; color: #0f0f0f; }
.header-sub { font-size: 14px; color: #666; margin: 0; }
.btn-primary {
  background: #3730a3; color: #fff; border-radius: 8px;
  padding: 10px 20px; font-size: 14px; font-weight: 600;
  text-decoration: none; white-space: nowrap;
}

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.stat-card {
  background: #fff; border-radius: 12px; padding: 20px;
  border: 1px solid #e5e5e5;
}
.stat-value { font-size: 28px; font-weight: 800; color: #1e1b4b; letter-spacing: -1px; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: #888; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.stat-change { font-size: 12px; font-weight: 600; }
.stat-change.up { color: #10b981; }
.stat-change.down { color: #dc2626; }

/* Content grid */
.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.section { background: #fff; border-radius: 12px; border: 1px solid #e5e5e5; padding: 24px; }
.section-head { margin-bottom: 20px; }
.section-head h2 { font-size: 16px; font-weight: 700; margin: 0; color: #0f0f0f; }

/* Activity */
.activity-list { display: flex; flex-direction: column; }
.activity-item {
  display: flex; align-items: center; gap: 14px;
  padding: 12px 0; border-bottom: 1px solid #f3f3f3;
}
.activity-item:last-child { border-bottom: none; }
.activity-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.activity-dot--quiz { background: #3730a3; }
.activity-dot--read { background: #10b981; }
.activity-body { flex: 1; }
.activity-title { font-size: 14px; font-weight: 500; color: #1e1b4b; }
.activity-meta { font-size: 12px; color: #aaa; margin-top: 2px; }
.activity-score { font-size: 14px; font-weight: 700; color: #3730a3; }

/* Suggestions */
.suggestion-list { display: flex; flex-direction: column; gap: 16px; }
.suggestion { padding: 14px; background: #f9f9ff; border-radius: 8px; border: 1px solid #ede9fe; }
.suggestion-tag { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #6366f1; margin-bottom: 6px; }
.suggestion-title { font-size: 14px; font-weight: 600; color: #1e1b4b; margin-bottom: 4px; }
.suggestion-meta { font-size: 12px; color: #aaa; margin-bottom: 10px; }
.suggestion-link { font-size: 13px; font-weight: 600; color: #3730a3; text-decoration: none; }
.suggestion-link:hover { text-decoration: underline; }

@media (max-width: 1100px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .content-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .dashboard { grid-template-columns: 1fr; }
  .sidebar { height: auto; position: static; }
  .main { padding: 24px 16px; }
}
</style>
