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
        <router-link to="/articles" class="nav-item nav-item--active">
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
        <h1>Articles</h1>
        <p class="header-sub">Read an article, then test your knowledge.</p>
      </header>

      <div class="filters">
        <div class="search-wrap">
          <span class="search-icon">⌕</span>
          <input v-model="search" class="search-input" type="text" placeholder="Search articles…" />
        </div>
        <div class="tag-pills">
          <button
            v-for="tag in tags"
            :key="tag"
            class="tag-pill"
            :class="{ 'tag-pill--active': activeTag === tag }"
            @click="activeTag = activeTag === tag ? '' : tag"
          >{{ tag }}</button>
        </div>
      </div>

      <div class="articles-grid">
        <div
          v-for="article in filteredArticles"
          :key="article.article_id"
          class="article-card"
        >
          <div class="article-meta">
            <span class="article-tag">{{ article.category }}</span>
          </div>
          <h2 class="article-title">{{ article.title }}</h2>
          <p class="article-excerpt">{{ article.content?.substring(0, 180) || 'Open this article to read more.' }}</p>
          <div class="article-footer">
            <router-link
                :to="`/article/${article.article_id}`"
                class="btn-read"
            >
                Read Article →
            </router-link>
           </div>
        </div>
      </div>

      <p v-if="filteredArticles.length === 0" class="empty-state">
        No articles match your search.
      </p>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const search = ref('')
const activeTag = ref('')

const tags = ['All', 'Data Protection', 'AI']

const articles = ref([])

onMounted(async () => {
    try{
        const response = await api.get('/articles')
        articles.value = response.data
    } catch (error) {
        console.error('Failed to load articles:', error)
    }
})

const filteredArticles = computed(() => {
    return articles.value.filter(article => {
    const matchTag =
      !activeTag.value ||
      activeTag.value === 'All' ||
      article.category === activeTag.value

    const matchSearch =
      !search.value ||
      article.title.toLowerCase().includes(search.value.toLowerCase())

    return matchTag && matchSearch
  })
})
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

.main { padding: 40px; }
.page-header { margin-bottom: 28px; }
.page-header h1 { font-size: 26px; font-weight: 800; margin: 0 0 4px; color: #0f0f0f; }
.header-sub { font-size: 14px; color: #666; margin: 0; }

.filters { display: flex; align-items: center; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.search-wrap { position: relative; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #aaa; font-size: 18px; }
.search-input {
  height: 40px; padding: 0 14px 0 36px; border: 1.5px solid #e5e5e5;
  border-radius: 8px; font-size: 14px; background: #fff; outline: none;
  width: 240px; transition: border-color 0.15s;
}
.search-input:focus { border-color: #3730a3; }
.tag-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.tag-pill {
  padding: 6px 14px; border-radius: 20px; border: 1.5px solid #e5e5e5;
  background: #fff; font-size: 13px; font-weight: 500; color: #666; cursor: pointer;
  transition: all 0.15s;
}
.tag-pill:hover { border-color: #3730a3; color: #3730a3; }
.tag-pill--active { background: #3730a3; border-color: #3730a3; color: #fff; }

.articles-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.article-card {
  background: #fff; border-radius: 12px; border: 1px solid #e5e5e5;
  padding: 24px; display: flex; flex-direction: column; gap: 12px;
  transition: box-shadow 0.15s;
}
.article-card:hover { box-shadow: 0 4px 20px rgba(55,48,163,0.08); }
.article-meta { display: flex; align-items: center; justify-content: space-between; }
.article-tag { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #6366f1; }
.article-read-time { font-size: 12px; color: #aaa; }
.article-title { font-size: 16px; font-weight: 700; color: #1e1b4b; margin: 0; line-height: 1.4; }
.article-excerpt { font-size: 14px; color: #666; line-height: 1.6; margin: 0; flex: 1; }
.article-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 4px; }
.article-date { font-size: 12px; color: #bbb; }
.btn-read { font-size: 13px; font-weight: 600; color: #3730a3; text-decoration: none; }
.btn-read:hover { text-decoration: underline; }

.empty-state { text-align: center; color: #aaa; font-size: 15px; margin-top: 48px; }

@media (max-width: 768px) {
  .page-layout { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .main { padding: 24px 16px; }
}
</style>
