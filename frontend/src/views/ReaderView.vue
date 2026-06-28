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
      <article class="article" ref="articleRef">
        <div class="article-meta">
          <span class="article-tag">{{ article.tag }}</span>
          <span class="article-dot">·</span>
          <span class="article-read-time">{{ article.readTime }} min read</span>
          <span class="article-dot">·</span>
          <span class="article-date">{{ article.date }}</span>
        </div>

        <h1 class="article-title">{{ article.title }}</h1>
        <p class="article-lede">{{ article.lede }}</p>

        <div class="article-body" v-html="article.body"></div>

        <div class="article-end">
          <div class="end-divider"></div>
          <p class="end-cta">You've finished the article. Ready to test your knowledge?</p>
          <button class="btn-primary btn-lg" @click="goToQuiz">Take the quiz →</button>
        </div>
      </article>

      <!-- Sticky sidebar -->
      <aside class="reader-aside">
        <div class="aside-card">
          <div class="aside-tag">{{ article.tag }}</div>
          <h2 class="aside-title">{{ article.title }}</h2>
          <div class="aside-stat">{{ article.readTime }} min read</div>
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

        <div class="aside-card aside-card--related">
          <h3>Read next</h3>
          <div class="related-list">
            <router-link
              v-for="r in relatedArticles"
              :key="r.id"
              :to="`/articles/${r.id}`"
              class="related-item"
            >
              <span class="related-tag">{{ r.tag }}</span>
              <span class="related-title">{{ r.title }}</span>
            </router-link>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const articleRef = ref(null)
const readProgress = ref(0)

const articleId = computed(() => parseInt(route.params.id))

const allArticles = [
  {
    id: 1,
    tag: 'Science',
    title: 'The Secret Life of Mitochondria',
    lede: 'Far more than just the powerhouse of the cell, mitochondria play a surprising role in signaling, immunity, and even aging.',
    readTime: 6,
    date: 'Jun 20, 2025',
    body: `
      <p>Every biology student learns the same line: mitochondria are the powerhouse of the cell. It's a satisfying simplification — a tiny furnace tucked inside each of your cells, burning glucose to produce ATP, the universal energy currency of life. But in the last two decades, researchers have discovered that this description barely scratches the surface.</p>

      <h2>More than energy</h2>
      <p>Mitochondria don't just make energy. They're active participants in signaling networks that regulate everything from cell death to inflammation. When a cell is under stress — infected by a virus, starved of oxygen, or simply aging — mitochondria broadcast chemical distress signals that can alter the behavior of the entire organism.</p>
      <p>One of the most striking findings is the role mitochondria play in apoptosis, the process of programmed cell death. When a cell decides it's time to die — because it's become cancerous, damaged beyond repair, or simply no longer needed — mitochondria release a protein called cytochrome c, which triggers the cell's self-destruct sequence. In a very real sense, mitochondria hold the keys to cellular life and death.</p>

      <h2>An ancient alliance</h2>
      <p>To understand why mitochondria are so deeply embedded in cellular life, you have to go back roughly two billion years. The leading theory — endosymbiosis — holds that mitochondria were originally free-living bacteria that were engulfed by a larger cell. Rather than being digested, the bacterium and its host struck a deal: the bacterium would supply energy, and the host would supply protection and resources.</p>
      <p>Over billions of years, most of the bacterial genome migrated into the host cell's nucleus, but mitochondria still retain a small genome of their own — a remnant of their independent past. This is why mitochondria have their own DNA, replicate independently within cells, and are inherited almost exclusively from the mother.</p>

      <h2>The aging connection</h2>
      <p>As we age, mitochondrial function declines. Mutations accumulate in mitochondrial DNA. The organelles become less efficient at producing ATP and more likely to leak reactive oxygen species — molecules that damage proteins, lipids, and DNA. This mitochondrial decay is now thought to be one of the primary drivers of aging itself.</p>
      <p>Researchers at the Salk Institute have shown that boosting mitochondrial quality control in aging mice can extend their healthy lifespan. Other labs are investigating whether compounds like NAD+ precursors — already popular as supplements — can meaningfully restore mitochondrial function in humans.</p>

      <h2>Mitochondria and the immune system</h2>
      <p>Perhaps the most surprising recent discovery is the role mitochondria play in immunity. When cells are damaged or dying, mitochondrial fragments can leak into the bloodstream, where immune cells interpret them as bacterial invaders — a consequence of mitochondria's ancient bacterial ancestry. This can trigger systemic inflammation, which helps explain why mitochondrial dysfunction is associated with inflammatory diseases ranging from lupus to Alzheimer's.</p>
      <p>Understanding this axis between mitochondria and inflammation has opened new therapeutic avenues. Several clinical trials are now testing drugs that target mitochondrial signaling as treatments for conditions once thought to be purely immunological.</p>

      <p>The humble powerhouse, it turns out, is running far more than just the lights.</p>
    `
  },
  {
    id: 2,
    tag: 'History',
    title: 'The Fall of Constantinople',
    lede: 'How a 53-day siege in 1453 ended the Byzantine Empire and reshaped the political map of the known world.',
    readTime: 9,
    date: 'Jun 18, 2025',
    body: `
      <p>On the morning of May 29, 1453, as Ottoman soldiers poured through a breach in the Theodosian Walls, the Byzantine Empire — the eastern continuation of Rome that had endured for over a thousand years — came to an end. The city of Constantinople, which had withstood countless sieges across its eleven centuries as a capital, finally fell. What followed reshaped the Mediterranean world and sent shockwaves that reached as far as the libraries of Florence and the courts of Western Europe.</p>

      <h2>The city on the edge</h2>
      <p>By the mid-fifteenth century, Constantinople was a shadow of its former self. The empire it governed had shrunk to little more than the city itself and a few coastal enclaves. Its population had collapsed from over half a million in its prime to perhaps 50,000. The walls that had held off Avars, Persians, Arabs, and Crusaders for centuries were still formidable, but the men and money to defend them were nearly gone.</p>
      <p>Emperor Constantine XI Palaiologos knew the odds. He sent desperate appeals to the Latin West, promising church union — a reunification of the Catholic and Orthodox churches that generations of Byzantines had resisted — in exchange for military aid. The response was a trickle: a handful of Genoese soldiers under Giovanni Giustiniani, and precious little else.</p>

      <h2>Mehmed's masterstroke</h2>
      <p>The young Ottoman sultan Mehmed II, just 21 years old, had been planning the assault for years. His key innovation was artillery. He commissioned a Hungarian engineer named Urban to build a cannon of unprecedented scale — capable of hurling stone balls weighing over half a ton. The Byzantines had been offered Urban's services first; they couldn't afford him.</p>
      <p>The siege began on April 6. Day after day, Mehmed's cannons pounded sections of the ancient walls. The defenders repaired breaches overnight by hand, but the effort was exhausting and the walls gradually weakened. In a feat of audacious logistics, Mehmed ordered his fleet dragged overland on greased logs to bypass the chain blocking the Golden Horn, opening a second front the defenders could barely cover.</p>

      <h2>The final assault</h2>
      <p>The decisive attack came before dawn on May 29. Three waves crashed against the walls. The first two — irregular troops — were beaten back with heavy losses. Then Mehmed sent in his Janissaries, elite soldiers drawn from Christian families as children and raised in strict Ottoman service. They found a small gate, the Kerkoporta, left inadvertently open. Within an hour, Ottoman flags flew from the towers.</p>
      <p>Constantine XI died fighting, his body never definitively identified. He is said to have torn off his imperial insignia and charged into the melee. Whether legendary or literal, it was an ending befitting the final emperor of Rome.</p>

      <h2>The aftermath</h2>
      <p>Mehmed entered the city on horseback and rode directly to the Hagia Sophia, the great cathedral that had stood since 537. He declared it a mosque. Later restored and converted to a museum in the twentieth century, it was reconverted to a mosque in 2020.</p>
      <p>The fall sent Greek scholars fleeing west with manuscripts that had been preserved in Constantinople for centuries — texts of Plato, Aristotle, and the ancient Greeks that were unknown or forgotten in Western Europe. Many historians credit this migration with accelerating the Italian Renaissance. The loss of the overland trade routes to the east also intensified European interest in finding a sea route to Asia, contributing to the Age of Exploration that would reshape the entire world within decades.</p>
    `
  },
  {
    id: 3,
    tag: 'Technology',
    title: 'How Large Language Models Work',
    lede: 'A plain-English explanation of transformers, attention mechanisms, and why GPT-4 can write poetry.',
    readTime: 8,
    date: 'Jun 16, 2025',
    body: `
      <p>In 2017, a team of researchers at Google published a paper titled "Attention Is All You Need." At the time, it was a modest-sounding contribution to a crowded field. Seven years later, the architecture it introduced — the transformer — underpins virtually every large language model in existence, from GPT-4 to Claude to Gemini. To understand how these systems work, you have to understand what a transformer is and why attention changed everything.</p>

      <h2>Before transformers: the problem with sequences</h2>
      <p>Language is inherently sequential. Words depend on the words before them. For decades, the dominant approach to language modeling used recurrent neural networks (RNNs), which processed text word by word, passing a "hidden state" from one step to the next — a running summary of everything seen so far.</p>
      <p>The problem was that this summary became lossy over long sequences. By the time the network reached word 200, its memory of word 1 had been compressed and distorted through 199 transformations. Long-range dependencies — the kind that matter when a pronoun at the end of a paragraph refers to a noun at the beginning — were hard to capture.</p>

      <h2>Attention: looking everywhere at once</h2>
      <p>The transformer solved this by abandoning sequential processing entirely. Instead of reading left to right, it looks at all words simultaneously and learns which ones are relevant to each other — a mechanism called self-attention.</p>
      <p>For each word, the model computes three vectors: a query ("what am I looking for?"), a key ("what do I contain?"), and a value ("what should I contribute?"). By comparing queries and keys across all positions, the model learns to weight how much each word should attend to every other word. The word "it" in a sentence can directly attend to "the cat" twelve words earlier without information having to pass through every intermediate step.</p>

      <h2>Scale and emergence</h2>
      <p>The transformer architecture was a breakthrough, but the most surprising discoveries came from scaling it up. When researchers began training transformers on billions of parameters using trillions of tokens of text, something unexpected happened: the models began exhibiting capabilities that weren't explicitly trained.</p>
      <p>This phenomenon — called emergent behavior — means that a model trained only to predict the next word in a sequence spontaneously learns to do arithmetic, write code, translate languages, and reason through multi-step problems. Nobody programmed these capabilities. They arose from scale.</p>

      <h2>What a language model actually is</h2>
      <p>At its core, a large language model is a very sophisticated next-token predictor. Given a sequence of text, it outputs a probability distribution over what the next word (or token) should be. That's it. Everything else — the apparent reasoning, the creativity, the ability to maintain a persona — is a consequence of this simple objective applied at enormous scale.</p>
      <p>When you ask GPT-4 a question, it doesn't "know" the answer in any human sense. It produces a sequence of tokens that, given its training, are statistically likely to follow your prompt. The remarkable thing is how often this produces useful, coherent, even insightful output — and how often it confidently produces plausible-sounding nonsense.</p>
    `
  },
]

const article = computed(() => allArticles.find(a => a.id === articleId.value) ?? allArticles[0])

const relatedArticles = computed(() =>
  allArticles.filter(a => a.id !== articleId.value).slice(0, 2)
)

function goToQuiz() {
  router.push({ path: '/quiz', query: { articleId: articleId.value } })
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

.article-lede {
  font-size: 20px; color: #555; line-height: 1.65;
  margin: 0 0 40px; font-weight: 400;
  border-left: 3px solid #3730a3; padding-left: 20px;
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
