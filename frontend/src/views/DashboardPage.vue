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
          <div class="avatar">AI</div>
          <div>
            <div class="user-name">{{ loadDetails.username }}</div>
            <div class="user-email">{{ loadDetails.email }}</div>
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
            <h2>External articles we think you should read</h2>
          </div>
          <div class="suggestion-list">
            <div class="suggestion" v-for="s in suggestions" :key="s.title">
              <div class="suggestion-tag">{{ s.tag }}</div>
              <div class="suggestion-title">{{ s.title }}</div>
              <div class="suggestion-meta">{{ s.readTime }} min read</div>
              <a
                :href="s.link"
                class="suggestion-link"
                target="_blank"
                rel="noopener noreferrer"
              >
                Read article →
             </a>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted,computed } from 'vue'
import api from '../services/api'

const suggestions = [
  { tag: 'Data Protection', title: 'How AI is changing data protection by Tech Target', readTime: 6, link: 'https://www.techtarget.com/data-technologies/tip/How-AI-is-changing-data-protection'},
  { tag: 'Data Lifecycle', title: 'Data Lifecycle Management: A Simple and Complete Explanation By Telmo Silva', readTime: 9, link:'https://www.clicdata.com/blog/complete-guide-data-lifecycle-management/' },
  { tag: 'Technology and Politics', title: 'How AI-generated disinformation might impact this year’s elections and how journalists should report on it By Marina Adami', readTime: 8, link: 'https://reutersinstitute.politics.ox.ac.uk/news/how-ai-generated-disinformation-might-impact-years-elections-and-how-journalists-should-report'},
]

const loadDetails = ref([])

onMounted(async () => {
    try{
        const response = await api.get('/loadDetails')
        loadDetails.value = response.data
    } catch (error) {
        console.error('Failed to load load users details', error)
    }
})


const results = ref([])

onMounted(async () => {
    try{
        const response = await api.get('/loadResults')
        results.value = response.data
    } catch (error) {
        console.error('Failed to load load users details', error)
    }
})

const activity = computed(() => {
    return results.value.map(result => ({
        result_id: result.result_id,
        type: 'quiz',
        title: `Quiz: ${result.article_title}`,
        meta: new Date(result.created_at).toLocaleString(),
        score: Math.round((result.score / result.max_score) * 100)
    }))
})

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

@media (max-width: 768px) {
  .dashboard { grid-template-columns: 1fr; }
  .sidebar { height: auto; position: static; }
  .main { padding: 24px 16px; }
}
</style>
