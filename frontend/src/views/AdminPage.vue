<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <router-link to="/" class="logo">Quizly</router-link>
        <span class="admin-badge">Admin</span>
      </div>
      <nav class="sidebar-nav">
        <button
          v-for="item in navItems"
          :key="item.key"
          class="nav-item"
          :class="{ 'nav-item--active': activeSection === item.key }"
          @click="activeSection = item.key"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          {{ item.label }}
        </button>
      </nav>
      <div class="sidebar-bottom">
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">←</span> Back to app
        </router-link>
      </div>
    </aside>

    <main class="main">
      <!-- Overview -->
      <section v-if="activeSection === 'overview'">
        <h1 class="page-title">Overview</h1>
        <div class="stats-row">
          <div class="stat-card" v-for="s in siteStats" :key="s.label">
            <div class="stat-value">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
        <div class="overview-grid">
          <div class="panel">
            <h2>Recent signups</h2>
            <table class="data-table">
              <thead>
                <tr><th>Name</th><th>Email</th><th>Joined</th><th>Quizzes</th></tr>
              </thead>
              <tbody>
                <tr v-for="u in recentUsers" :key="u.email">
                  <td><strong>{{ u.name }}</strong></td>
                  <td class="muted">{{ u.email }}</td>
                  <td class="muted">{{ u.joined }}</td>
                  <td>{{ u.quizzes }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="panel">
            <h2>Top articles</h2>
            <div class="top-list">
              <div class="top-item" v-for="(a, i) in topArticles" :key="a.title">
                <span class="top-rank">{{ i + 1 }}</span>
                <div class="top-body">
                  <div class="top-title">{{ a.title }}</div>
                  <div class="top-meta">{{ a.views }} views · {{ a.quizzes }} quizzes taken</div>
                </div>
                <div class="top-score">{{ a.avgScore }}%</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Articles management -->
      <section v-if="activeSection === 'articles'">
        <div class="section-header">
          <h1 class="page-title">Articles</h1>
          <button class="btn-primary" @click="showArticleModal = true">+ New article</button>
        </div>
        <div class="panel">
          <div class="table-toolbar">
            <input v-model="articleSearch" class="search-input" type="text" placeholder="Search articles…" />
            <select v-model="articleFilter" class="select-input">
              <option value="">All tags</option>
              <option v-for="tag in articleTags" :key="tag" :value="tag">{{ tag }}</option>
            </select>
          </div>
          <table class="data-table">
            <thead>
              <tr><th>Title</th><th>Tag</th><th>Status</th><th>Views</th><th>Avg score</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="a in filteredAdminArticles" :key="a.id">
                <td><strong>{{ a.title }}</strong></td>
                <td><span class="tag-chip">{{ a.tag }}</span></td>
                <td><span class="status-chip" :class="`status-chip--${a.status}`">{{ a.status }}</span></td>
                <td class="muted">{{ a.views }}</td>
                <td>{{ a.avgScore }}%</td>
                <td>
                  <div class="row-actions">
                    <button class="row-btn">Edit</button>
                    <button class="row-btn row-btn--danger">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Users management -->
      <section v-if="activeSection === 'users'">
        <div class="section-header">
          <h1 class="page-title">Users</h1>
          <span class="count-label">{{ adminUsers.length }} total</span>
        </div>
        <div class="panel">
          <input v-model="userSearch" class="search-input" type="text" placeholder="Search users by name or email…" style="margin-bottom: 16px" />
          <table class="data-table">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Role</th><th>Joined</th><th>Quizzes</th><th>Avg score</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="u in filteredUsers" :key="u.email">
                <td>
                  <div class="user-cell">
                    <div class="user-avatar">{{ u.name.split(' ').map(n => n[0]).join('') }}</div>
                    <strong>{{ u.name }}</strong>
                  </div>
                </td>
                <td class="muted">{{ u.email }}</td>
                <td><span class="role-chip" :class="`role-chip--${u.role}`">{{ u.role }}</span></td>
                <td class="muted">{{ u.joined }}</td>
                <td>{{ u.quizzes }}</td>
                <td>{{ u.avgScore }}%</td>
                <td>
                  <div class="row-actions">
                    <button class="row-btn">View</button>
                    <button class="row-btn row-btn--danger">Ban</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Quiz questions management -->
      <section v-if="activeSection === 'quizzes'">
        <div class="section-header">
          <h1 class="page-title">Quiz questions</h1>
          <button class="btn-primary">+ New question</button>
        </div>
        <div class="panel">
          <table class="data-table">
            <thead>
              <tr><th>Question</th><th>Article</th><th>Difficulty</th><th>Correct rate</th><th></th></tr>
            </thead>
            <tbody>
              <tr v-for="q in quizQuestions" :key="q.id">
                <td class="question-cell">{{ q.text }}</td>
                <td class="muted">{{ q.article }}</td>
                <td><span class="diff-chip" :class="`diff-chip--${q.difficulty}`">{{ q.difficulty }}</span></td>
                <td>
                  <div class="correct-bar-wrap">
                    <div class="correct-bar">
                      <div class="correct-fill" :style="{ width: q.correctRate + '%', background: correctColor(q.correctRate) }"></div>
                    </div>
                    <span>{{ q.correctRate }}%</span>
                  </div>
                </td>
                <td>
                  <div class="row-actions">
                    <button class="row-btn">Edit</button>
                    <button class="row-btn row-btn--danger">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- New article modal -->
    <div class="modal-backdrop" v-if="showArticleModal" @click.self="showArticleModal = false">
      <div class="modal">
        <h2>New article</h2>
        <div class="form-grid">
          <div class="field field--full">
            <label>Title</label>
            <input type="text" placeholder="Article title…" />
          </div>
          <div class="field">
            <label>Tag</label>
            <select class="select-input">
              <option v-for="tag in articleTags" :key="tag">{{ tag }}</option>
            </select>
          </div>
          <div class="field">
            <label>Read time (min)</label>
            <input type="number" value="5" min="1" />
          </div>
          <div class="field field--full">
            <label>Content</label>
            <textarea rows="6" placeholder="Write or paste the article content…"></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-outline" @click="showArticleModal = false">Cancel</button>
          <button class="btn-primary" @click="showArticleModal = false">Save article</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeSection = ref('overview')
const showArticleModal = ref(false)
const articleSearch = ref('')
const articleFilter = ref('')
const userSearch = ref('')

const navItems = [
  { key: 'overview', icon: '⊞', label: 'Overview' },
  { key: 'articles', icon: '◫', label: 'Articles' },
  { key: 'users', icon: '◯', label: 'Users' },
  { key: 'quizzes', icon: '✦', label: 'Quiz questions' },
]

const siteStats = [
  { label: 'Total users', value: '12,481' },
  { label: 'Articles published', value: '348' },
  { label: 'Quizzes taken today', value: '1,204' },
  { label: 'Avg. score (30d)', value: '79%' },
]

const recentUsers = [
  { name: 'Priya Nair', email: 'priya@example.com', joined: 'Jun 23, 2025', quizzes: 2 },
  { name: 'Tom Becker', email: 'tom@example.com', joined: 'Jun 22, 2025', quizzes: 7 },
  { name: 'Sofia Melo', email: 'sofia@example.com', joined: 'Jun 22, 2025', quizzes: 4 },
  { name: 'James Park', email: 'james@example.com', joined: 'Jun 21, 2025', quizzes: 11 },
  { name: 'Aiko Tanaka', email: 'aiko@example.com', joined: 'Jun 20, 2025', quizzes: 3 },
]

const topArticles = [
  { title: 'How Large Language Models Work', views: 8420, quizzes: 3102, avgScore: 74 },
  { title: 'The Fall of Constantinople', views: 6710, quizzes: 2488, avgScore: 81 },
  { title: 'What Happens When You Sleep', views: 5990, quizzes: 2310, avgScore: 88 },
  { title: 'The Secret Life of Mitochondria', views: 4830, quizzes: 1902, avgScore: 76 },
]

const articleTags = ['Science', 'History', 'Technology', 'Culture', 'Health']

const adminArticles = [
  { id: 1, title: 'How Large Language Models Work', tag: 'Technology', status: 'published', views: 8420, avgScore: 74 },
  { id: 2, title: 'The Fall of Constantinople', tag: 'History', status: 'published', views: 6710, avgScore: 81 },
  { id: 3, title: 'The Philosophy of Boredom', tag: 'Culture', status: 'published', views: 3210, avgScore: 69 },
  { id: 4, title: 'CRISPR: Gene Editing Explained', tag: 'Science', status: 'draft', views: 0, avgScore: 0 },
  { id: 5, title: 'The Quantum Internet', tag: 'Technology', status: 'draft', views: 0, avgScore: 0 },
]

const filteredAdminArticles = computed(() => {
  return adminArticles.filter(a => {
    const matchSearch = !articleSearch.value || a.title.toLowerCase().includes(articleSearch.value.toLowerCase())
    const matchTag = !articleFilter.value || a.tag === articleFilter.value
    return matchSearch && matchTag
  })
})

const adminUsers = [
  { name: 'Alex Rivera', email: 'alex@example.com', role: 'admin', joined: 'Jan 3, 2025', quizzes: 47, avgScore: 82 },
  { name: 'Priya Nair', email: 'priya@example.com', role: 'user', joined: 'Jun 23, 2025', quizzes: 2, avgScore: 71 },
  { name: 'Tom Becker', email: 'tom@example.com', role: 'user', joined: 'Jun 22, 2025', quizzes: 7, avgScore: 78 },
  { name: 'Sofia Melo', email: 'sofia@example.com', role: 'user', joined: 'Jun 22, 2025', quizzes: 4, avgScore: 65 },
  { name: 'James Park', email: 'james@example.com', role: 'user', joined: 'Jun 21, 2025', quizzes: 11, avgScore: 90 },
  { name: 'Aiko Tanaka', email: 'aiko@example.com', role: 'user', joined: 'Jun 20, 2025', quizzes: 3, avgScore: 55 },
]

const filteredUsers = computed(() => {
  const q = userSearch.value.toLowerCase()
  return adminUsers.filter(u => !q || u.name.toLowerCase().includes(q) || u.email.toLowerCase().includes(q))
})

const quizQuestions = [
  { id: 1, text: 'In what year did Constantinople fall to Ottoman forces?', article: 'The Fall of Constantinople', difficulty: 'easy', correctRate: 88 },
  { id: 2, text: 'Which emperor ruled during the fall of Constantinople?', article: 'The Fall of Constantinople', difficulty: 'medium', correctRate: 61 },
  { id: 3, text: 'What is the primary function of the transformer architecture in LLMs?', article: 'How Large Language Models Work', difficulty: 'hard', correctRate: 44 },
  { id: 4, text: 'What stage of sleep is most associated with memory consolidation?', article: 'What Happens When You Sleep', difficulty: 'medium', correctRate: 72 },
  { id: 5, text: 'What bacterial system inspired CRISPR gene editing?', article: 'CRISPR: Gene Editing Explained', difficulty: 'hard', correctRate: 38 },
]

function correctColor(rate) {
  if (rate >= 75) return '#10b981'
  if (rate >= 50) return '#f59e0b'
  return '#dc2626'
}
</script>

<style scoped>
.admin-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  background: #f5f5f0;
}

.sidebar {
  background: #0f0e2a; display: flex; flex-direction: column;
  position: sticky; top: 0; height: 100vh;
}
.sidebar-logo {
  padding: 24px 20px 18px; border-bottom: 1px solid rgba(255,255,255,0.07);
  display: flex; align-items: center; gap: 10px;
}
.logo { font-weight: 800; font-size: 18px; color: #fff; text-decoration: none; }
.admin-badge {
  font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  background: #3730a3; color: #a5b4fc; padding: 2px 7px; border-radius: 4px;
}
.sidebar-nav { flex: 1; padding: 12px 10px; display: flex; flex-direction: column; gap: 2px; }
.nav-item {
  display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px;
  font-size: 13px; font-weight: 500; color: #818cf8; cursor: pointer;
  background: none; border: none; text-align: left; width: 100%;
  text-decoration: none; transition: background 0.15s, color 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.nav-item--active { background: rgba(99,102,241,0.2); color: #fff; }
.nav-icon { font-size: 14px; width: 18px; text-align: center; }
.sidebar-bottom { padding: 12px 10px; border-top: 1px solid rgba(255,255,255,0.07); }

.main { padding: 36px 40px; }
.page-title { font-size: 24px; font-weight: 800; margin: 0 0 24px; color: #1e1b4b; }
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.section-header .page-title { margin-bottom: 0; }
.count-label { font-size: 13px; color: #aaa; }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 28px; }
.stat-card { background: #fff; border-radius: 10px; border: 1px solid #e5e5e5; padding: 18px 20px; }
.stat-value { font-size: 26px; font-weight: 900; color: #1e1b4b; letter-spacing: -1px; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }

/* Overview grid */
.overview-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

/* Panel */
.panel { background: #fff; border-radius: 12px; border: 1px solid #e5e5e5; padding: 24px; margin-bottom: 20px; }
.panel h2 { font-size: 15px; font-weight: 700; margin: 0 0 18px; }

/* Table */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th {
  text-align: left; padding: 0 12px 12px; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.5px; color: #aaa;
  border-bottom: 1px solid #f0f0f0;
}
.data-table td { padding: 13px 12px; border-bottom: 1px solid #f8f8f8; vertical-align: middle; }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover { background: #fafaf8; }
.muted { color: #999; }
.question-cell { max-width: 320px; }

/* Chips */
.tag-chip {
  background: #ede9fe; color: #5b21b6; font-size: 11px; font-weight: 600;
  padding: 3px 8px; border-radius: 4px; letter-spacing: 0.3px;
}
.status-chip { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.status-chip--published { background: #dcfce7; color: #15803d; }
.status-chip--draft { background: #f3f4f6; color: #6b7280; }
.role-chip { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.role-chip--admin { background: #ede9fe; color: #5b21b6; }
.role-chip--user { background: #f3f4f6; color: #6b7280; }
.diff-chip { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.diff-chip--easy { background: #dcfce7; color: #15803d; }
.diff-chip--medium { background: #fef9c3; color: #854d0e; }
.diff-chip--hard { background: #fee2e2; color: #991b1b; }

/* Row actions */
.row-actions { display: flex; gap: 6px; }
.row-btn {
  padding: 4px 10px; border-radius: 6px; border: 1px solid #e5e5e5;
  background: #fff; font-size: 12px; font-weight: 600; color: #555; cursor: pointer; transition: all 0.15s;
}
.row-btn:hover { border-color: #3730a3; color: #3730a3; }
.row-btn--danger { color: #dc2626; }
.row-btn--danger:hover { border-color: #dc2626; color: #dc2626; background: #fef2f2; }

/* User cell */
.user-cell { display: flex; align-items: center; gap: 10px; }
.user-avatar {
  width: 28px; height: 28px; background: #3730a3; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; font-weight: 700; color: #fff; flex-shrink: 0;
}

/* Correct rate bar */
.correct-bar-wrap { display: flex; align-items: center; gap: 8px; }
.correct-bar { width: 64px; height: 5px; background: #e5e5e5; border-radius: 3px; overflow: hidden; }
.correct-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }

/* Toolbar */
.table-toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.search-input {
  height: 36px; padding: 0 12px; border: 1.5px solid #e5e5e5;
  border-radius: 8px; font-size: 13px; outline: none; background: #fff; flex: 1;
  transition: border-color 0.15s;
}
.search-input:focus { border-color: #3730a3; }
.select-input {
  height: 36px; padding: 0 12px; border: 1.5px solid #e5e5e5;
  border-radius: 8px; font-size: 13px; background: #fff; outline: none; cursor: pointer;
}

/* Buttons */
.btn-primary {
  background: #3730a3; color: #fff; border: none; border-radius: 8px;
  padding: 9px 18px; font-size: 13px; font-weight: 700; cursor: pointer; transition: background 0.15s;
}
.btn-primary:hover { background: #312e81; }
.btn-outline {
  background: #fff; color: #444; border: 1.5px solid #d1d5db; border-radius: 8px;
  padding: 9px 18px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s;
}
.btn-outline:hover { border-color: #3730a3; color: #3730a3; }

/* Top list */
.top-list { display: flex; flex-direction: column; gap: 14px; }
.top-item { display: flex; align-items: center; gap: 12px; }
.top-rank { font-size: 14px; font-weight: 800; color: #d1d5db; width: 18px; flex-shrink: 0; }
.top-body { flex: 1; }
.top-title { font-size: 13px; font-weight: 600; color: #1e1b4b; }
.top-meta { font-size: 12px; color: #aaa; margin-top: 2px; }
.top-score { font-size: 14px; font-weight: 700; color: #3730a3; }

/* Modal */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal { background: #fff; border-radius: 16px; padding: 36px; max-width: 520px; width: 90%; }
.modal h2 { font-size: 20px; font-weight: 800; margin: 0 0 24px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 28px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field--full { grid-column: 1 / -1; }
.field label { font-size: 13px; font-weight: 600; color: #444; }
.field input, .field select, .field textarea {
  padding: 9px 12px; border: 1.5px solid #d1d5db; border-radius: 8px;
  font-size: 14px; background: #fff; outline: none; font-family: inherit; resize: vertical;
  transition: border-color 0.15s;
}
.field input:focus, .field select:focus, .field textarea:focus { border-color: #3730a3; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

@media (max-width: 1100px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); }
  .overview-grid { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .admin-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .main { padding: 24px 16px; }
}
</style>
