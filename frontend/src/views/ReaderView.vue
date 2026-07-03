<template>
  <div class="reader-page">
    <!-- Top bar -->
    <header class="reader-header">
      <router-link to="/articles" class="back-link">
        <span class="back-arrow">←</span> All articles
      </router-link>
      <div class="progress-wrap">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: readProgress + '%' }"></div>
        </div>
        <span class="progress-label">{{ Math.round(readProgress) }}% read</span>
      </div>
      <button class="btn-quiz" @click="goToQuiz">Take the quiz →</button>
    </header>

    <div class="reader-layout" ref="layoutRef">
      <!-- Article -->
      <article v-if="article" class="article" ref="articleRef">

        <div class="article-meta">
          <span class="article-tag">{{ article.category }}</span>
        </div>

        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-body" v-html="article.content"></div>

        <div class="article-end">
          <div class="end-divider"></div>
          <p class="end-cta">You've finished the article. Ready to test your knowledge?</p>
          <button class="btn-primary btn-lg" @click="goToQuiz">Take the quiz →</button>
        </div>
      </article>

      <!-- Sticky sidebar -->
      <aside v-if="article" class="reader-aside">
        <div class="aside-card">
          <div class="aside-tag">{{ article.category }}</div>
          <h2 class="aside-title">{{ article.title }}</h2>
          <div class="aside-progress">
            <div class="aside-progress-label">
              <span>Reading progress</span>
              <span>{{ Math.round(readProgress) }}%</span>
            </div>
            <div class="aside-progress-bar">
              <div class="aside-progress-fill" :style="{ width: readProgress + '%' }"></div>
            </div>
          </div>
          <button class="btn-primary btn-full" @click="goToQuiz">Take the quiz →</button>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const article = ref(null)

const route = useRoute()
const router = useRouter()
const articleRef = ref(null)
const readProgress = ref(0)
const layoutRef = ref(null)

onMounted(async () => {
  try {
    const response = await api.get(`/articles/${route.params.id}`)
    article.value = response.data
    console.log(response.data)
  } catch (err) {
    console.error(err)
  }
})

function goToQuiz() {
  router.push({
    path: '/quiz',
    query: {
      articleId: route.params.id
    }
  })
}

function onScroll() {
  const el = articleRef.value
  if (!el) return
  const { top, height } = el.getBoundingClientRect()
  const windowH = window.innerHeight
  const scrolled = Math.max(0, windowH - top)
  readProgress.value = Math.min(100, (scrolled / height) * 100)
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.reader-page {
  min-height: 100vh;
  background: #fafaf8;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Header */
.reader-header {
  position: sticky; top: 0; z-index: 10;
  background: #fff; border-bottom: 1px solid #e5e5e5;
  padding: 0 40px; height: 58px;
  display: flex; align-items: center; gap: 24px;
}
.back-link {
  display: flex; align-items: center; gap: 6px;
  font-size: 14px; font-weight: 500; color: #3730a3; text-decoration: none;
  white-space: nowrap; transition: opacity 0.15s;
}
.back-link:hover { opacity: 0.7; }
.back-arrow { font-size: 16px; }

.progress-wrap { flex: 1; display: flex; align-items: center; gap: 12px; }
.progress-bar { flex: 1; height: 5px; background: #e5e5e5; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: #3730a3; border-radius: 3px; transition: width 0.2s; }
.progress-label { font-size: 12px; color: #aaa; white-space: nowrap; }

.btn-quiz {
  background: #3730a3; color: #fff; border: none; border-radius: 8px;
  padding: 9px 18px; font-size: 13px; font-weight: 700; cursor: pointer;
  white-space: nowrap; transition: background 0.15s;
}
.btn-quiz:hover { background: #312e81; }

/* Layout */
.reader-layout {
  max-width: 1100px; margin: 0 auto; padding: 56px 40px 80px;
  display: grid; grid-template-columns: 1fr 300px; gap: 64px; align-items: start;
}

/* Article */
.article-meta {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 20px;
}
.article-tag { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #6366f1; }
.article-dot { color: #d1d5db; font-size: 14px; }
.article-read-time, .article-date { font-size: 13px; color: #aaa; }

.article-title {
  font-size: clamp(28px, 4vw, 44px); font-weight: 900;
  color: #1e1b4b; line-height: 1.15; letter-spacing: -1px;
  margin: 0 0 20px;
}

.article-body {
  font-size: 17px; line-height: 1.8; color: #2d2d2d;
}

.article-body :deep(h2) {
  font-size: 22px; font-weight: 800; color: #1e1b4b;
  margin: 48px 0 16px; letter-spacing: -0.3px;
}
.article-body :deep(p) {
  margin: 0 0 24px;
}

/* Article end */
.article-end { margin-top: 56px; text-align: center; padding: 48px 0 0; }
.end-divider { width: 60px; height: 3px; background: #3730a3; margin: 0 auto 32px; border-radius: 2px; }
.end-cta { font-size: 18px; color: #555; margin: 0 0 24px; }

.btn-primary {
  background: #3730a3; color: #fff; border: none; border-radius: 8px;
  font-size: 15px; font-weight: 700; cursor: pointer; transition: background 0.15s;
  padding: 13px 28px; display: inline-block;
}
.btn-primary:hover { background: #312e81; }
.btn-lg { padding: 16px 36px; font-size: 17px; }
.btn-full { width: 100%; padding: 13px 0; }

/* Aside */
.reader-aside { position: sticky; top: 74px; display: flex; flex-direction: column; gap: 16px; }

.aside-card {
  background: #fff; border: 1px solid #e5e5e5; border-radius: 14px; padding: 22px;
}
.aside-tag { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #6366f1; margin-bottom: 8px; }
.aside-title { font-size: 16px; font-weight: 800; color: #1e1b4b; line-height: 1.3; margin: 0 0 10px; }
.aside-stat { font-size: 13px; color: #aaa; margin-bottom: 18px; }

.aside-progress { margin-bottom: 18px; }
.aside-progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #888; margin-bottom: 6px; }
.aside-progress-bar { height: 5px; background: #e5e5e5; border-radius: 3px; overflow: hidden; }
.aside-progress-fill { height: 100%; background: #3730a3; border-radius: 3px; transition: width 0.2s; }

.aside-card--related h3 { font-size: 13px; font-weight: 700; color: #888; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 14px; }
.related-list { display: flex; flex-direction: column; gap: 12px; }
.related-item { display: flex; flex-direction: column; gap: 3px; text-decoration: none; padding: 10px; border-radius: 8px; transition: background 0.15s; }
.related-item:hover { background: #f5f3ff; }
.related-tag { font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #6366f1; }
.related-title { font-size: 13px; font-weight: 600; color: #1e1b4b; line-height: 1.4; }

@media (max-width: 960px) {
  .reader-layout { grid-template-columns: 1fr; }
  .reader-aside { display: none; }
  .reader-header { padding: 0 20px; }
  .reader-layout { padding: 40px 20px 60px; }
}
</style>
