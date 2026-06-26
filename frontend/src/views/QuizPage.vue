<template>
  <div class="quiz-page">
    <!-- Header -->
    <header class="quiz-header">
      <router-link to="/articles" class="back-link">← Back to articles</router-link>
      <div class="quiz-progress-wrap">
        <div class="quiz-progress-bar">
          <div class="quiz-progress-fill" :style="{ width: progressPct + '%' }"></div>
        </div>
        <span class="progress-label">{{ currentIndex + 1 }} / {{ questions.length }}</span>
      </div>
      <div class="timer" :class="{ 'timer--warn': timeLeft <= 10 }">{{ formatTime(timeLeft) }}</div>
    </header>

    <!-- Quiz body -->
    <div class="quiz-body" v-if="!finished">
      <div class="question-meta">
        <span class="question-tag">{{ currentQuestion.tag }}</span>
        <span class="question-num">Question {{ currentIndex + 1 }}</span>
      </div>
      <h1 class="question-text">{{ currentQuestion.text }}</h1>

      <div class="options">
        <button
          v-for="(option, i) in currentQuestion.options"
          :key="i"
          class="option"
          :class="optionClass(i)"
          :disabled="answered"
          @click="selectAnswer(i)"
        >
          <span class="option-letter">{{ letters[i] }}</span>
          <span class="option-text">{{ option }}</span>
          <span class="option-indicator" v-if="answered && i === currentQuestion.correct">✓</span>
          <span class="option-indicator option-indicator--wrong" v-if="answered && selectedIndex === i && i !== currentQuestion.correct">✗</span>
        </button>
      </div>

      <div class="explanation" v-if="answered && currentQuestion.explanation">
        <strong>Explanation:</strong> {{ currentQuestion.explanation }}
      </div>

      <div class="question-actions">
        <button class="btn-next" v-if="answered" @click="nextQuestion">
          {{ currentIndex < questions.length - 1 ? 'Next question →' : 'See results →' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const letters = ['A', 'B', 'C', 'D']

const questions = [
  {
    tag: 'History',
    text: 'In what year did Constantinople fall to Ottoman forces under Sultan Mehmed II?',
    options: ['1389', '1453', '1492', '1521'],
    correct: 1,
    explanation: 'The siege lasted 53 days and ended on 29 May 1453, marking the end of the Byzantine Empire.'
  },
  {
    tag: 'History',
    text: 'Which Byzantine emperor was ruling during the fall of Constantinople?',
    options: ['Basil II', 'Alexios I Komnenos', 'Constantine XI Palaiologos', 'John VIII Palaiologos'],
    correct: 2,
    explanation: 'Constantine XI Palaiologos was the last reigning Byzantine emperor, dying in the final defense of the city.'
  },
  {
    tag: 'History',
    text: 'What strategic advantage did the Ottomans use to breach the city\'s legendary walls?',
    options: ['Naval blockade alone', 'Tunnel mining', 'Large-caliber cannon artillery', 'Biological warfare'],
    correct: 2,
    explanation: 'Mehmed employed massive cannons, including the famous Basilica cannon, to pound the Theodosian Walls.'
  },
  {
    tag: 'History',
    text: 'The fall of Constantinople is commonly cited as one marker of the end of which historical era?',
    options: ['The Ancient World', 'The Middle Ages', 'The Renaissance', 'The Early Modern Period'],
    correct: 1,
    explanation: 'Many historians use 1453 as a conventional end date for the Middle Ages in Europe, alongside 1492 and other events.'
  },
  {
    tag: 'History',
    text: 'What name did the Ottomans give to Constantinople after its conquest?',
    options: ['Adrianople', 'Bursa', 'Istanbul', 'Edirne'],
    correct: 2,
    explanation: 'The city gradually came to be known as Istanbul, a name that became official in 1930 under Atatürk\'s westernization reforms.'
  },
]

const currentIndex = ref(0)
const selectedIndex = ref(null)
const answered = ref(false)
const scores = ref([])
const finished = ref(false)
const timeLeft = ref(30)
let timer = null

const currentQuestion = computed(() => questions[currentIndex.value])
const progressPct = computed(() => ((currentIndex.value) / questions.length) * 100)

function formatTime(s) {
  return s < 10 ? `0:0${s}` : `0:${s}`
}

function startTimer() {
  clearInterval(timer)
  timeLeft.value = 30
  timer = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      clearInterval(timer)
      if (!answered.value) {
        answered.value = true
        scores.value.push(false)
      }
    }
  }, 1000)
}

function selectAnswer(i) {
  if (answered.value) return
  selectedIndex.value = i
  answered.value = true
  clearInterval(timer)
  scores.value.push(i === currentQuestion.value.correct)
}

function optionClass(i) {
  if (!answered.value) return ''
  if (i === currentQuestion.value.correct) return 'option--correct'
  if (i === selectedIndex.value) return 'option--wrong'
  return 'option--dim'
}

function nextQuestion() {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++
    selectedIndex.value = null
    answered.value = false
    startTimer()
  } else {
    finished.value = true
    router.push({ name: 'Summary', query: { correct: scores.value.filter(Boolean).length, total: questions.length } })
  }
}

onMounted(startTimer)
onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.quiz-page {
  min-height: 100vh;
  background: #fafaf8;
  font-family: 'Inter', system-ui, sans-serif;
  display: flex;
  flex-direction: column;
}

.quiz-header {
  display: flex; align-items: center; gap: 24px;
  padding: 16px 40px; border-bottom: 1px solid #e5e5e5;
  background: #fff; position: sticky; top: 0; z-index: 10;
}
.back-link { font-size: 14px; font-weight: 500; color: #3730a3; text-decoration: none; white-space: nowrap; }
.back-link:hover { text-decoration: underline; }

.quiz-progress-wrap { flex: 1; display: flex; align-items: center; gap: 12px; }
.quiz-progress-bar { flex: 1; height: 6px; background: #e5e5e5; border-radius: 3px; overflow: hidden; }
.quiz-progress-fill { height: 100%; background: #3730a3; border-radius: 3px; transition: width 0.4s; }
.progress-label { font-size: 13px; color: #888; white-space: nowrap; }

.timer {
  font-size: 20px; font-weight: 800; color: #1e1b4b;
  font-variant-numeric: tabular-nums; min-width: 44px; text-align: right;
}
.timer--warn { color: #dc2626; }

.quiz-body {
  max-width: 720px; margin: 0 auto; padding: 60px 32px;
  flex: 1; width: 100%; box-sizing: border-box;
}

.question-meta { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.question-tag { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #6366f1; }
.question-num { font-size: 13px; color: #aaa; }

.question-text {
  font-size: clamp(20px, 3vw, 28px); font-weight: 800;
  color: #1e1b4b; line-height: 1.35; margin: 0 0 40px;
  letter-spacing: -0.3px;
}

.options { display: flex; flex-direction: column; gap: 12px; margin-bottom: 28px; }
.option {
  display: flex; align-items: center; gap: 16px;
  padding: 16px 20px; border-radius: 10px;
  border: 2px solid #e5e5e5; background: #fff;
  text-align: left; cursor: pointer; transition: all 0.15s; width: 100%;
}
.option:hover:not(:disabled) { border-color: #3730a3; background: #f5f3ff; }
.option:disabled { cursor: default; }
.option--correct { border-color: #10b981; background: #ecfdf5; }
.option--wrong { border-color: #dc2626; background: #fef2f2; }
.option--dim { opacity: 0.45; }

.option-letter {
  width: 32px; height: 32px; border-radius: 50%;
  background: #f3f3f5; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #555; flex-shrink: 0;
}
.option--correct .option-letter { background: #10b981; color: #fff; }
.option--wrong .option-letter { background: #dc2626; color: #fff; }
.option-text { flex: 1; font-size: 15px; font-weight: 500; color: #1e1b4b; }
.option-indicator { font-size: 18px; font-weight: 700; color: #10b981; }
.option-indicator--wrong { color: #dc2626; }

.explanation {
  background: #fffbeb; border: 1px solid #fcd34d; border-radius: 8px;
  padding: 14px 18px; font-size: 14px; color: #78350f; line-height: 1.6;
  margin-bottom: 28px;
}

.question-actions { display: flex; justify-content: flex-end; }
.btn-next {
  background: #3730a3; color: #fff; border: none; border-radius: 8px;
  padding: 14px 28px; font-size: 15px; font-weight: 700; cursor: pointer;
  transition: background 0.15s;
}
.btn-next:hover { background: #312e81; }

@media (max-width: 600px) {
  .quiz-header { padding: 16px 20px; }
  .quiz-body { padding: 32px 20px; }
}
</style>
