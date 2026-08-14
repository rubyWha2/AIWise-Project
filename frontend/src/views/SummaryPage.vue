<template>
  <div class="summary-page">
    <div class="summary-card">
      <!-- Score ring -->
      <div class="score-ring-wrap">
        <svg class="score-ring" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r="52" fill="none" stroke="#e8e5ff" stroke-width="10" />
          <circle
            cx="60" cy="60" r="52" fill="none"
            :stroke="scoreColor"
            stroke-width="10"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="dashOffset"
            transform="rotate(-90 60 60)"
            style="transition: stroke-dashoffset 1s ease"
          />
        </svg>
        <div class="score-label">
          <span class="score-pct">{{ scorePercent }}%</span>
          <span class="score-sub">{{ correct }}/{{ total }} correct</span>
        </div>
      </div>

      <div class="grade-badge" :style="{ background: scoreColor }">{{ grade }}</div>
      <h1 class="summary-title">{{ headline }}</h1>
      <p class="summary-sub">{{ subline }}</p>

      <div class="summary-stats">
        <div class="sstat">
          <div class="sstat-val">{{ correct }}</div>
          <div class="sstat-lbl">Correct</div>
        </div>
        <div class="sstat">
          <div class="sstat-val">{{ total - correct }}</div>
          <div class="sstat-lbl">Incorrect</div>
        </div>
        <div class="sstat">
          <div class="sstat-val">{{ timeSpent }}s</div>
          <div class="sstat-lbl">Avg. per Q</div>
        </div>
      </div>

      <div class="summary-actions">
        <router-link to="/articles" class="btn-secondary">Browse more articles</router-link>
        <router-link to="/quiz" class="btn-primary">Retry quiz</router-link>
      </div>
    </div>

    <div class="xp-banner">
      <span class="xp-icon">⚡</span>
      <span>You earned <strong>+{{ xp }} XP</strong> from this quiz!</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()

const correct = computed(() => Number(route.query.correct ?? 0))
const total = computed(() => Number(route.query.maxScore ?? 0))
const totalTime = computed(() => Number(route.query.totalTime ?? 0))

const timeSpent = computed(() => {
  if (total.value === 0) return 0
  return Math.round(totalTime.value / total.value)
})

const scorePercent = computed(() => Math.round((correct.value / total.value) * 100))
const circumference = 2 * Math.PI * 52

const dashOffset = computed(() => {
  return circumference - (scorePercent.value / 100) * circumference
})

const scoreColor = computed(() => {
  if (scorePercent.value >= 80) return '#10b981'
  if (scorePercent.value >= 60) return '#f59e0b'
  return '#dc2626'
})

const grade = computed(() => {
  if (scorePercent.value >= 90) return 'A'
  if (scorePercent.value >= 80) return 'B'
  if (scorePercent.value >= 70) return 'C'
  if (scorePercent.value >= 60) return 'D'
  return 'F'
})

const headline = computed(() => {
  if (scorePercent.value >= 90) return 'Outstanding!'
  if (scorePercent.value >= 70) return 'Well done!'
  if (scorePercent.value >= 50) return 'Not bad!'
  return 'Keep practicing!'
})

const subline = computed(() => {
  if (scorePercent.value >= 90) return "You clearly read every word. Excellent retention."
  if (scorePercent.value >= 70) return "Solid understanding. Review the missed questions to sharpen up."
  if (scorePercent.value >= 50) return "You've got the basics. Read the article again to reinforce the details."
  return "Don't be discouraged — each attempt builds your knowledge."
})

const xp = computed(() => correct.value * 20 + (scorePercent.value === 100 ? 50 : 0))
</script>

<style scoped>
.summary-page {
  min-height: 100vh;
  background: #f5f5f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  font-family: 'Inter', system-ui, sans-serif;
  gap: 20px;
}

.summary-card {
  background: #fff;
  border-radius: 20px;
  border: 1px solid #e5e5e5;
  padding: 48px 40px;
  max-width: 440px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
}

.score-ring-wrap {
  position: relative;
  width: 160px;
  height: 160px;
  margin-bottom: 8px;
}
.score-ring { width: 100%; height: 100%; }
.score-label {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.score-pct { font-size: 32px; font-weight: 900; color: #1e1b4b; letter-spacing: -1px; }
.score-sub { font-size: 13px; color: #aaa; }

.grade-badge {
  width: 48px; height: 48px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 900; color: #fff;
}

.summary-title { font-size: 28px; font-weight: 800; color: #1e1b4b; margin: 0; letter-spacing: -0.5px; }
.summary-sub { font-size: 15px; color: #666; line-height: 1.6; margin: 0; max-width: 320px; }

.summary-stats {
  display: flex;
  gap: 0;
  width: 100%;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  overflow: hidden;
  margin: 8px 0;
}
.sstat {
  flex: 1;
  padding: 16px 12px;
  border-right: 1px solid #e5e5e5;
  text-align: center;
}
.sstat:last-child { border-right: none; }
.sstat-val { font-size: 22px; font-weight: 800; color: #1e1b4b; }
.sstat-lbl { font-size: 12px; color: #aaa; margin-top: 2px; }

.summary-actions { display: flex; gap: 12px; width: 100%; }
.btn-primary, .btn-secondary {
  flex: 1; padding: 13px 0; border-radius: 8px;
  font-size: 14px; font-weight: 700; text-decoration: none;
  text-align: center; transition: all 0.15s;
}
.btn-primary { background: #3730a3; color: #fff; }
.btn-primary:hover { background: #312e81; }
.btn-secondary { background: #f3f3f5; color: #1e1b4b; }
.btn-secondary:hover { background: #e8e8f0; }

.xp-banner {
  background: #1e1b4b; color: #a5b4fc;
  border-radius: 12px; padding: 14px 24px;
  font-size: 14px; display: flex; align-items: center; gap: 10px;
  max-width: 440px; width: 100%;
}
.xp-banner strong { color: #fff; }
.xp-icon { font-size: 18px; }

@media (max-width: 480px) {
  .summary-card { padding: 32px 24px; }
  .summary-actions { flex-direction: column; }
}
</style>
