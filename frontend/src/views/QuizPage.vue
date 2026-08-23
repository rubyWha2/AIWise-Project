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
    <div
        class="quiz-body"
        v-if="!finished && questions.length > 0"
    >
      <div class="question-meta">
        <span class="question-tag">{{ currentQuestion.title }}</span>
        <span class="question-num">Question {{ currentIndex + 1 }}</span>
      </div>
      <h1 class="question-text">{{ currentQuestion.question }}</h1>


      <div class="options">
  <button
    v-for="letter in letters"
    :key="letter"
    class="option"
    :class="optionClass(letter)"
    :disabled="answered"
    @click="selectAnswer(letter)"
  >
    <span class="option-letter">{{ letter }}</span>

    <span class="option-text">
      {{ currentQuestion[`option_${letter.toLowerCase()}`] }}
    </span>

    <span
      class="option-indicator"
      v-if="answered && letter === currentQuestion.correct_answer"
    >
      ✓
    </span>

    <span
      class="option-indicator option-indicator--wrong"
      v-if="answered &&
             selectedAnswer === letter &&
             letter !== currentQuestion.correct_answer"
    >
      ✗
    </span>
  </button>
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
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const route = useRoute()
const questions = ref([])

const articleId = route.query.articleId

// Pull the quiz questions for the article that sent the user here.
onMounted(async () => {
  try {
    const response = await api.get(`/quiz/${articleId}`)

    questions.value = response.data
    console.log(questions.value.length)
    console.log(questions.value)

    console.log(response.data)
  } catch (err) {
    console.error(err)
  }
})


const letters = ['a', 'b', 'c', 'd']

const score = ref(0)
const maxScore = computed(() => questions.value.length)
const currentIndex = ref(0)
const selectedAnswer = ref(null)
const answered = ref(false)
const scores = ref([])
const finished = ref(false)
const timeLeft = ref(30)
let timer = null
const totalTime = ref(0)

const currentQuestion = computed(() => questions.value[currentIndex.value])

// Progress is based on the current question index rather than answered count.
const progressPct = computed(() =>
  questions.value.length
    ? (currentIndex.value / questions.value.length) * 100
    : 0
)

function formatTime(s) {
  return s < 10 ? `0:0${s}` : `0:${s}`
}

// Reset and run the per-question countdown.
function startTimer() {
  clearInterval(timer)
  timeLeft.value = 30
  timer = setInterval(() => {
    timeLeft.value--
    totalTime.value++

    if (timeLeft.value <= 0) {
      clearInterval(timer)
      if (!answered.value) {
        answered.value = true
        scores.value.push(false)
      }
    }
  }, 1000)
}

// Lock the selected answer so each question can only be scored once.
function selectAnswer(answer) {
  if (answered.value) return

  answered.value = true
  selectedAnswer.value = answer

  clearInterval(timer)

  if (answer === currentQuestion.value.correct_answer) {
    score.value++
  }
}

// Drives the visual feedback for correct, incorrect, and non-selected answers.
function optionClass(letter) {
  if (!answered.value) return ''

  if (letter === currentQuestion.value.correct_answer)
    return 'option--correct'

  if (letter === selectedAnswer.value)
    return 'option--wrong'

  return 'option--dim'
}

// Move through the quiz until the final question, then persist the score.
async function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    selectedAnswer.value = null
    answered.value = false
    startTimer()
  } else {
    finished.value = true
    await finishQuiz()
  }
}

// Store the result before routing to the summary screen.
async function finishQuiz() {
  try {
    const response = await api.post('/updateResults', {
      article_id: articleId,
      score: score.value,
      max_score: maxScore.value
    })

    console.log('Result saved:', response.data)

    router.push({
      name: 'Summary',
      query: {
        correct: score.value,
        maxScore: maxScore.value,
        articleId: articleId
      }
    })

  } catch (e) {
    console.error('Failed to save result:', e)
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
