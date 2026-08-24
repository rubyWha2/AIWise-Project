<template>
  <div class="landing">
    <nav class="nav">
      <div class="nav-inner">
        <span class="logo">AiWise</span>
        <div class="nav-links">
          <router-link to="/login" class="nav-link">Log in</router-link>
          <router-link to="/register" class="btn-primary">Get started</router-link>
        </div>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-inner">
        <div class="hero-tag">Keep your business protected in the age of AI</div>
        <h1 class="hero-headline">Read. Test.<br /><em>Protect.</em></h1>
        <p class="hero-sub">
          AIWise pairs curated articles with adaptive quizzes so every session
          moves you closer towards helping you master operating your business and stay compliant with evolving digital legislation.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="btn-primary btn-lg">Start for free</router-link>
          <router-link to="/login" class="btn-ghost btn-lg">Sign in</router-link>
        </div>
      </div>

      <div class="hero-visual">
      </div>
    </section>

    <section class="features">
      <div class="features-inner">
        <h2 class="section-title">How it works</h2>
        <div class="features-grid">
          <router-link to="/login" class="feature">
            <div class="feature-num">01</div>
            <h3>Read an article</h3>
            <p>Browse our curated library across science, history, technology, and culture.</p>
          </router-link>
          <router-link to="/login" class="feature">
            <div class="feature-num">02</div>
            <h3>Take the quiz</h3>
            <p>Answer adaptive questions generated from the article's core concepts.</p>
          </router-link>
          <router-link to="/login" class="feature">
            <div class="feature-num">03</div>
            <h3>Track your growth</h3>
            <p>See your scores improve and build a streak that keeps you coming back.</p>
          </router-link>
        </div>
      </div>
    </section>

    <section class="cta-band">
      <div class="cta-band-inner">
        <h2>Ready to protect your business and employees?</h2>
        <router-link to="/register" class="btn-primary btn-lg">Create free account</router-link>
      </div>
    </section>

    <footer class="footer">
      <div class="footer-inner">

        <span class="logo">AiWise</span>

        <div class="footer-links">
          <router-link to="/privacy">Privacy</router-link>
        </div>
        <div class="footer-links">
          <router-link to="/Terms">Terms of Service </router-link>
        </div>
        <span class="footer-copy">&copy; 2026 AiWise. All rights reserved.</span>
      </div>
    </footer>

<!-- Cookie popup -->
    <div
      v-if="showCookieNotice"
      class="cookie-overlay"
    >
      <div class="cookie-modal">

        <div class="cookie-icon"></div>

        <h2>Cookies on AIWise</h2>

        <p>
          AIWise uses an essential cookie to keep you signed in and provide
          core account functionality.
        </p>

        <p class="cookie-small">
          We do not use advertising cookies.
        </p>

        <button
          class="cookie-btn"
          @click="acceptCookies"
        >
          Got it
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showCookieNotice = ref(false)

onMounted(() => {
  // Only show the cookie message until the visitor accepts it once in this browser.
  const accepted = localStorage.getItem('cookieNoticeAccepted')

  if (!accepted) {
    showCookieNotice.value = true
  }
})

const acceptCookies = () => {
  // Store the acceptance locally because the notice is informational only.
  localStorage.setItem('cookieNoticeAccepted', 'true')
  showCookieNotice.value = false
}

</script>

<style scoped>

.landing {
  font-family: 'Inter', system-ui, sans-serif;
  color: #0f0f0f;
  background: #fafaf8;
  min-height: 100vh;
}

/* Nav */
.nav { border-bottom: 1px solid #e5e5e5; background: #fafaf8; position: sticky; top: 0; z-index: 10; }
.nav-inner { max-width: 1160px; margin: 0 auto; padding: 0 32px; height: 60px; display: flex; align-items: center; justify-content: space-between; }
.logo { font-weight: 800; font-size: 20px; letter-spacing: -0.5px; color: #3730a3; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-link { color: #555; font-size: 14px; text-decoration: none; transition: color 0.15s; }
.nav-link:hover { color: #3730a3; }

/* Buttons */
.btn-primary { background: #3730a3; color: #fff; border-radius: 8px; padding: 10px 20px; font-size: 14px; font-weight: 600; text-decoration: none; transition: background 0.15s; display: inline-block; }
.btn-primary:hover { background: #312e81; }
.btn-ghost { color: #3730a3; border: 1.5px solid #3730a3; border-radius: 8px; padding: 10px 20px; font-size: 14px; font-weight: 600; text-decoration: none; transition: background 0.15s; display: inline-block; }
.btn-ghost:hover { background: #eef2ff; }
.btn-lg { padding: 14px 28px; font-size: 16px; }

/* Hero */
.hero {
  min-height: 85vh;
  position: relative;

  background-image: url('/AIWiseLanding.jpg');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: 70% center;

  display: flex;
  align-items: center;

  padding: 80px 32px;
}

/* Fade the image behind the text */
.hero::before {
  content: "";
  position: absolute;
  inset: 0;

  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0.98) 30%,
    rgba(255, 255, 255, 0.75) 45%,
    rgba(255, 255, 255, 0.15) 70%,
    rgba(255, 255, 255, 0) 100%
  );

  z-index: 0;
}

/* Main hero container */
.hero-inner {
  position: relative;
  z-index: 1;

  width: 100%;
  max-width: 1160px;

  margin: 0 auto;
}

/* Keep ALL text on the left */
.hero-content {
  width: 50%;
  max-width: 560px;
}

/* Small heading */
.hero-tag {
  margin-bottom: 18px;

  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;

  color: #3730a3;
}

/* Main heading */
.hero-headline {
  margin: 0 0 24px;

  font-size: clamp(48px, 6vw, 76px);
  line-height: 0.98;
  font-weight: 800;

  color: #1e1b4b;
}

.hero-headline em {
  font-style: italic;
  color: #3730a3;
}

/* Description */
.hero-sub {
  max-width: 520px;

  margin: 0 0 32px;

  font-size: 17px;
  line-height: 1.7;

  color: #555;
}

/* Buttons */
.hero-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Floating card */
.hero-visual {
  position: absolute;

  right: 0;
  top: 50%;

  transform: translateY(-50%);

  width: 360px;
}

.card-float {
  padding: 22px;

  background: rgba(255, 255, 255, 0.94);

  border-radius: 16px;

  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);

  backdrop-filter: blur(8px);
}

.stat-num {
  display: block;

  margin-bottom: 10px;

  font-size: 15px;
  line-height: 1.4;
  font-weight: 700;

  color: #1e1b4b;
}

.stat-label {
  display: block;

  font-size: 12px;
  line-height: 1.5;

  color: #666;
}

/* Features */
.features { border-top: 1px solid #e5e5e5; padding: 80px 32px; }
.features-inner { max-width: 1160px; margin: 0 auto; }
.section-title { font-size: 14px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #888; margin: 0 0 48px; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 48px; }
.feature { color: inherit; text-decoration: none; }
.feature:hover h3 { color: #3730a3; }
.feature-num { font-size: 48px; font-weight: 900; color: #e8e5ff; letter-spacing: -2px; margin-bottom: 12px; }
.feature h3 { font-size: 20px; font-weight: 700; margin: 0 0 10px; }
.feature p { font-size: 15px; color: #666; line-height: 1.7; margin: 0; }

/* CTA Band */
.cta-band { background: #3730a3; padding: 72px 32px; }
.cta-band-inner { max-width: 1160px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 32px; flex-wrap: wrap; }
.cta-band h2 { font-size: clamp(24px, 3vw, 36px); font-weight: 800; color: #fff; margin: 0; letter-spacing: -0.5px; }
.cta-band .btn-primary { background: #fff; color: #3730a3; }
.cta-band .btn-primary:hover { background: #eef2ff; }

/* Footer */
.footer { border-top: 1px solid #e5e5e5; padding: 24px 32px; }
.footer-inner { max-width: 1160px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.footer-copy { font-size: 13px; color: #aaa; }

.cookie-overlay {
  position: fixed;
  inset: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  background: rgba(15, 15, 30, 0.55);

  z-index: 9999;
}

.cookie-modal {
  width: 90%;
  max-width: 440px;

  background: white;

  padding: 32px;

  border-radius: 16px;

  text-align: center;

  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.cookie-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.cookie-modal h2 {
  margin: 0 0 12px;

  color: #1e1b4b;

  font-size: 22px;
}

.cookie-modal p {
  color: #555;

  font-size: 14px;
  line-height: 1.6;

  margin-bottom: 10px;
}

.cookie-small {
  font-size: 12px !important;
  color: #888 !important;
}

.cookie-btn {
  margin-top: 16px;

  width: 100%;

  padding: 12px 20px;

  border: none;
  border-radius: 8px;

  background: #3730a3;
  color: white;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;
}

.cookie-btn:hover {
  background: #312e81;
}

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
  .features-grid { grid-template-columns: 1fr; gap: 32px; }
  .cta-band-inner { flex-direction: column; text-align: center; }
}
</style>
