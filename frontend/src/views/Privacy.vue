<template>
  <div class="policy-page">
    <!-- Minimal nav -->
    <header class="policy-nav">
      <router-link to="/" class="logo">AiWise</router-link>
      <router-link to="/register" class="nav-cta">Get started</router-link>
    </header>

    <div class="policy-layout">
      <!-- Sticky table of contents -->
      <aside class="toc">
        <div class="toc-inner">
          <p class="toc-heading">On this page</p>
          <nav>
            <a
              v-for="section in sections"
              :key="section.id"
              :href="`#${section.id}`"
              class="toc-link"
              :class="{ 'toc-link--active': activeSection === section.id }"
              @click.prevent="scrollTo(section.id)"
            >{{ section.title }}</a>
          </nav>
          <div class="toc-contact">
            <p class="toc-contact-label">Questions?</p>
            <a href="mailto:aiwisenotifications@gmail.com" class="toc-email">aiwisenotifications@gmail.com</a>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <main class="policy-content" ref="contentRef">
        <!-- Hero -->
        <div class="policy-hero">
          <div class="policy-badge">Legal</div>
          <h1>Privacy Policy <span class="amp">&</span> GDPR</h1>
          <p class="policy-intro">
            The AiWise Development Team is committed to protecting your privacy and ensuring your personal
            data is handled securely and in compliance with data protection laws, including the
            <strong>General Data Protection Regulation (GDPR)</strong> and the
            <strong>Data Protection Act 2018</strong>.
          </p>
          <div class="policy-meta">
            <span class="meta-item">
              <span class="meta-icon">📅</span>
              Last updated: 28 August 2026
            </span>
            <span class="meta-item">
              <span class="meta-icon">🏢</span>
              AiWise Development Team
            </span>
          </div>
        </div>

        <!-- Sections -->
        <section
          v-for="section in sections"
          :key="section.id"
          :id="section.id"
          class="policy-section"
          ref="sectionRefs"
        >
          <div class="section-num">{{ section.num }}</div>
          <h2>{{ section.title }}</h2>
          <div class="section-body" v-html="section.body"></div>
        </section>

        <!-- GDPR Rights highlight -->
        <section id="your-rights" class="policy-section rights-section">
          <div class="section-num">06</div>
          <h2>Your Data Protection Rights</h2>
          <p class="rights-intro">Under GDPR, you have the following rights:</p>
          <div class="rights-grid">
            <div class="right-card" v-for="right in rights" :key="right.title">
              <span class="right-icon">✓</span>
              <div>
                <div class="right-title">{{ right.title }}</div>
                <div class="right-desc">{{ right.desc }}</div>
              </div>
            </div>
          </div>
        </section>

        <!-- Contact section -->
        <section id="contact-us" class="policy-section contact-section">
          <div class="section-num">07</div>
          <h2>Contact Us</h2>
          <p>
            If you have any questions about this policy or wish to exercise your data rights,
            please contact us:
          </p>
          <a href="mailto:aiwisenotifications@gmail.com" class="contact-card">
            <span class="contact-icon">✉</span>
            <div>
              <div class="contact-label">Email us</div>
              <div class="contact-email">aiwisenotifications@gmail.com</div>
            </div>
            <span class="contact-arrow">→</span>
          </a>
        </section>

        <!-- Footer note -->
        <div class="policy-footer-note">
          This Privacy Policy is reviewed regularly and updated as necessary to ensure compliance
          with data protection laws. Last Updated: <strong>28 August 2026</strong>.
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const activeSection = ref('information-we-collect')
const contentRef = ref(null)
const sectionRefs = ref([])

const sections = [
  {
    id: 'information-we-collect',
    num: '01',
    title: 'Information We Collect',
    body: `
      <p>We may collect and process the following types of personal data:</p>
      <ul>
        <li><strong>Personal details</strong> — name and email address</li>
        <li><strong>Communications</strong> — when you contact us via email or website forms</li>
        <li><strong>Website usage data</strong> — cookies, IP addresses, and analytics to improve our website experience</li>
      </ul>
    `
  },
  {
    id: 'how-we-use',
    num: '02',
    title: 'How We Use Your Information',
    body: `
      <p>We only use your personal data for the following purposes:</p>
      <ul>
        <li>To provide a secure education experience</li>
        <li>To improve our website and services through analytics and feedback</li>
      </ul>
    `
  },
  {
    id: 'how-we-protect',
    num: '03',
    title: 'How We Protect Your Data',
    body: `
      <p>We take your data security seriously and implement:</p>
      <ul>
        <li>Secure storage and encryption of sensitive information</li>
        <li>Access controls to limit who can view your data</li>
        <li>Regular reviews of our data protection policies</li>
      </ul>
    `
  },
  {
    id: 'sharing',
    num: '04',
    title: 'Sharing Your Information',
    body: `
      <p>We do not sell or share your personal data with third parties, except:</p>
      <ul>
        <li>When required by law or regulatory bodies</li>
        <li>With trusted service providers who assist in delivering our services (who comply with data protection laws)</li>
        <li>With your explicit consent</li>
      </ul>
    `
  },
  {
    id: 'cookies',
    num: '05',
    title: 'Cookies and Website Tracking',
    body: `
      <p>
        We use cookies to enhance your browsing experience. These help us understand website
        traffic and improve our services. You can adjust your cookie settings in your browser
        at any time.
      </p>
    `
  },
]

const rights = [
  { title: 'Access', desc: 'Request a copy of the data we hold about you.' },
  { title: 'Correction', desc: 'Ask us to update or correct your information.' },
  { title: 'Deletion', desc: 'Request the removal of your data where legally possible.' },
  { title: 'Restriction', desc: 'Limit how we process your data.' },
  { title: 'Objection', desc: 'Object to how we use your data.' },
  { title: 'Data Portability', desc: 'Request your data in a format that can be transferred to another service.' },
]

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  activeSection.value = id
}

function onScroll() {
  const allIds = [...sections.map(s => s.id), 'your-rights', 'contact-us']
  for (const id of [...allIds].reverse()) {
    const el = document.getElementById(id)
    if (el && el.getBoundingClientRect().top <= 120) {
      activeSection.value = id
      break
    }
  }
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.policy-page {
  min-height: 100vh;
  background: #fafaf8;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Nav */
.policy-nav {
  position: sticky; top: 0; z-index: 10;
  background: #fff; border-bottom: 1px solid #e5e5e5;
  padding: 0 40px; height: 58px;
  display: flex; align-items: center; justify-content: space-between;
}
.logo { font-weight: 900; font-size: 20px; color: #3730a3; text-decoration: none; letter-spacing: -0.5px; }
.nav-cta {
  background: #3730a3; color: #fff; border-radius: 8px;
  padding: 8px 18px; font-size: 13px; font-weight: 700; text-decoration: none;
  transition: background 0.15s;
}
.nav-cta:hover { background: #312e81; }

/* Layout */
.policy-layout {
  max-width: 1100px; margin: 0 auto; padding: 0 40px 80px;
  display: grid; grid-template-columns: 220px 1fr; gap: 64px; align-items: start;
}

/* TOC */
.toc { position: sticky; top: 80px; padding-top: 56px; }
.toc-inner { display: flex; flex-direction: column; gap: 0; }
.toc-heading { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #aaa; margin: 0 0 14px; }
.toc-link {
  display: block; font-size: 13px; font-weight: 500; color: #888;
  text-decoration: none; padding: 7px 0 7px 12px;
  border-left: 2px solid transparent;
  transition: all 0.15s; line-height: 1.4;
}
.toc-link:hover { color: #3730a3; }
.toc-link--active { color: #3730a3; border-left-color: #3730a3; font-weight: 600; }

.toc-contact { margin-top: 32px; padding-top: 20px; border-top: 1px solid #e5e5e5; }
.toc-contact-label { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #aaa; margin: 0 0 6px; }
.toc-email { font-size: 12px; color: #3730a3; font-weight: 600; text-decoration: none; word-break: break-all; }
.toc-email:hover { text-decoration: underline; }

/* Content */
.policy-content { padding-top: 56px; }

/* Hero */
.policy-hero { margin-bottom: 56px; }
.policy-badge {
  display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase; color: #6366f1; background: #eef2ff;
  padding: 4px 12px; border-radius: 20px; margin-bottom: 16px;
}
h1 {
  font-size: clamp(32px, 4vw, 48px); font-weight: 900; color: #1e1b4b;
  letter-spacing: -1.5px; line-height: 1.1; margin: 0 0 20px;
}
.amp { color: #3730a3; }
.policy-intro { font-size: 17px; color: #555; line-height: 1.7; margin: 0 0 24px; max-width: 600px; }
.policy-meta { display: flex; gap: 24px; flex-wrap: wrap; }
.meta-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #888; }
.meta-icon { font-size: 14px; }

/* Sections */
.policy-section {
  padding: 40px 0;
  border-top: 1px solid #e5e5e5;
  scroll-margin-top: 80px;
}
.section-num {
  font-size: 11px; font-weight: 800; letter-spacing: 2px;
  text-transform: uppercase; color: #d1d5db; margin-bottom: 10px;
}
.policy-section h2 {
  font-size: 22px; font-weight: 800; color: #1e1b4b;
  letter-spacing: -0.3px; margin: 0 0 18px;
}
.section-body { font-size: 15px; color: #555; line-height: 1.75; }
.section-body :deep(p) { margin: 0 0 14px; }
.section-body :deep(p:last-child) { margin-bottom: 0; }
.section-body :deep(ul) { margin: 0; padding-left: 0; list-style: none; display: flex; flex-direction: column; gap: 10px; }
.section-body :deep(li) {
  display: flex; align-items: flex-start; gap: 10px; padding: 12px 16px;
  background: #f9f9ff; border: 1px solid #ede9fe; border-radius: 8px;
  font-size: 14px; color: #444; line-height: 1.5;
}
.section-body :deep(li)::before {
  content: '→'; color: #6366f1; font-weight: 700; flex-shrink: 0; margin-top: 1px;
}
.section-body :deep(strong) { color: #1e1b4b; }

/* Rights grid */
.rights-section { }
.rights-intro { font-size: 15px; color: #555; margin: 0 0 20px; }
.rights-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.right-card {
  display: flex; align-items: flex-start; gap: 12px;
  background: #fff; border: 1px solid #e5e5e5; border-radius: 10px;
  padding: 16px 18px; transition: border-color 0.15s, box-shadow 0.15s;
}
.right-card:hover { border-color: #a5b4fc; box-shadow: 0 2px 12px rgba(55,48,163,0.06); }
.right-icon {
  width: 28px; height: 28px; background: #ecfdf5; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; color: #10b981; font-weight: 800; flex-shrink: 0;
}
.right-title { font-size: 14px; font-weight: 700; color: #1e1b4b; margin-bottom: 3px; }
.right-desc { font-size: 13px; color: #777; line-height: 1.5; }

/* Contact */
.contact-section p { font-size: 15px; color: #555; line-height: 1.7; margin: 0 0 20px; }
.contact-card {
  display: flex; align-items: center; gap: 16px;
  background: #1e1b4b; border-radius: 12px; padding: 20px 24px;
  text-decoration: none; transition: background 0.15s;
}
.contact-card:hover { background: #2d2a6e; }
.contact-icon {
  width: 44px; height: 44px; background: rgba(255,255,255,0.1); border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.contact-label { font-size: 12px; color: #a5b4fc; font-weight: 600; margin-bottom: 3px; }
.contact-email { font-size: 15px; color: #fff; font-weight: 700; }
.contact-arrow { margin-left: auto; font-size: 20px; color: #a5b4fc; }

/* Footer note */
.policy-footer-note {
  margin-top: 48px; padding: 20px 24px;
  background: #f5f3ff; border: 1px solid #ede9fe; border-radius: 10px;
  font-size: 13px; color: #666; line-height: 1.6;
}

@media (max-width: 900px) {
  .policy-layout { grid-template-columns: 1fr; padding: 0 20px 60px; }
  .toc { display: none; }
  .rights-grid { grid-template-columns: 1fr; }
  .policy-nav { padding: 0 20px; }
}
</style>
