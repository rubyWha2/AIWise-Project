<template>
  <div class="policy-page">
    <!-- Minimal nav -->
    <header class="policy-nav">
      <router-link to="/" class="logo">AIWise</router-link>
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
            >
              {{ section.title }}
            </a>

            <a
              href="#contact-us"
              class="toc-link"
              :class="{ 'toc-link--active': activeSection === 'contact-us' }"
              @click.prevent="scrollTo('contact-us')"
            >
              Contact Us
            </a>
          </nav>

          <div class="toc-contact">
            <p class="toc-contact-label">Questions?</p>
            <a
              href="mailto:aiwisenotifications@gmail.com"
              class="toc-email"
            >
              aiwisenotifications@gmail.com
            </a>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <main class="policy-content" ref="contentRef">
        <!-- Hero -->
        <div class="policy-hero">
          <div class="policy-badge">Legal</div>

          <h1>Terms of Use</h1>

          <p class="policy-intro">
            These Terms of Use explain the rules that apply when accessing and
            using AIWise, including our articles, quizzes, accounts and other
            educational features.
          </p>

          <div class="policy-meta">
            <span class="meta-item">
              <span class="meta-icon">📅</span>
              Last updated: 22 August 2026
            </span>

            <span class="meta-item">
              <span class="meta-icon">🏢</span>
              AIWise Development Team
            </span>
          </div>
        </div>

        <!-- Sections -->
        <section
          v-for="section in sections"
          :key="section.id"
          :id="section.id"
          class="policy-section"
        >
          <div class="section-num">{{ section.num }}</div>
          <h2>{{ section.title }}</h2>
          <div class="section-body" v-html="section.body"></div>
        </section>

        <!-- Contact section -->
        <section
          id="contact-us"
          class="policy-section contact-section"
        >
          <div class="section-num">13</div>

          <h2>Contact Us</h2>

          <p>
            If you have any questions about these Terms of Use, please contact
            us:
          </p>

          <a
            href="mailto:aiwisenotifications@gmail.com"
            class="contact-card"
          >
            <span class="contact-icon">✉</span>

            <div>
              <div class="contact-label">Email us</div>
              <div class="contact-email">
                aiwisenotifications@gmail.com
              </div>
            </div>

            <span class="contact-arrow">→</span>
          </a>
        </section>

        <!-- Footer note -->
        <div class="policy-footer-note">
          These Terms of Use may be reviewed and updated as AIWise develops.
          Last updated: <strong>22 August 2026</strong>.
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const activeSection = ref('about-aiwise')
const contentRef = ref(null)

const sections = [
  {
    id: 'about-aiwise',
    num: '01',
    title: 'About AIWise',
    body: `
      <p>
        AIWise is an educational platform designed to help users learn about
        topics including artificial intelligence, data protection, digital
        legislation and business compliance through articles, quizzes and
        related educational content.
      </p>

      <p>
        AIWise is currently operated as a personal portfolio and educational
        project by the AIWise Development Team.
      </p>
    `
  },

  {
    id: 'educational-information',
    num: '02',
    title: 'Educational Information',
    body: `
      <p>
        Information provided through AIWise is intended for general educational
        and informational purposes only.
      </p>

      <p>
        Content provided by AIWise should not be considered legal, financial,
        regulatory or other professional advice.
      </p>

      <p>
        Although reasonable efforts are made to provide accurate and useful
        information, laws, regulations and official guidance can change.
        Users should consult appropriate professional advice or official
        sources before making business, legal or compliance decisions.
      </p>
    `
  },

  {
    id: 'user-accounts',
    num: '03',
    title: 'User Accounts',
    body: `
      <p>
        Some AIWise features require you to create an account.
      </p>

      <ul>
        <li>You should provide accurate information when creating and maintaining your account.</li>
        <li>You are responsible for maintaining the security of your account.</li>
        <li>You must not attempt to access another user's account without authorisation.</li>
        <li>You must not use AIWise for unlawful, fraudulent or malicious purposes.</li>
      </ul>
    `
  },

  {
    id: 'acceptable-use',
    num: '04',
    title: 'Acceptable Use',
    body: `
      <p>When using AIWise, you must not:</p>

      <ul>
        <li>Attempt to gain unauthorised access to AIWise, its database, user accounts or underlying systems.</li>
        <li>Attempt to interfere with the security or normal operation of the website.</li>
        <li>Use automated systems in a way that excessively accesses, disrupts or damages the service.</li>
        <li>Use AIWise for unlawful, fraudulent or malicious purposes.</li>
        <li>Attempt to exploit vulnerabilities or circumvent security or access controls.</li>
      </ul>
    `
  },

  {
    id: 'account-suspension',
    num: '05',
    title: 'Account Suspension',
    body: `
      <p>
        AIWise may restrict or suspend an account where there is reasonable
        evidence that the account has been used in violation of these Terms
        of Use or poses a security risk to the service or other users.
      </p>

      <p>
        Where appropriate, account access may be restored after the reason
        for the restriction has been resolved.
      </p>
    `
  },

  {
    id: 'external-content',
    num: '06',
    title: 'Articles and External Sources',
    body: `
      <p>
        AIWise may contain references or links to articles, research,
        guidance and websites operated by third parties.
      </p>

      <p>
        External websites are not controlled by AIWise. AIWise is not
        responsible for the availability, accuracy, content or privacy
        practices of third-party websites.
      </p>

      <p>
        Links and references to external sources are provided for
        informational and educational purposes.
      </p>
    `
  },

  {
    id: 'quiz-results',
    num: '07',
    title: 'Quiz Results and Learning Progress',
    body: `
      <p>
        Quiz scores, progress information, streaks and other learning
        statistics provided by AIWise are intended for educational purposes.
      </p>

      <p>
        Results provided through AIWise should not be interpreted as
        professional qualifications, certifications or evidence that an
        individual or organisation complies with any particular law or
        regulation.
      </p>
    `
  },

  {
    id: 'intellectual-property',
    num: '08',
    title: 'Intellectual Property',
    body: `
      <p>
        The AIWise name, original website design, original software and
        original content are protected by applicable intellectual property
        laws.
      </p>

      <p>
        Third-party articles, trademarks, publications and other materials
        remain the property of their respective owners.
      </p>

      <p>
        You may use AIWise for personal and educational purposes. You may
        not reproduce or redistribute substantial parts of the service
        without permission where permission is required.
      </p>
    `
  },

  {
    id: 'availability',
    num: '09',
    title: 'Service Availability',
    body: `
      <p>
        AIWise is provided on an "as available" basis.
      </p>

      <p>
        The service may occasionally become unavailable because of
        maintenance, technical problems, development changes or
        circumstances outside our control.
      </p>

      <p>
        As AIWise is currently a portfolio project, continued or
        uninterrupted availability of the service is not guaranteed.
      </p>
    `
  },

  {
    id: 'liability',
    num: '10',
    title: 'Limitation of Liability',
    body: `
      <p>
        To the extent permitted by law, AIWise is not responsible for losses
        arising solely from reliance on educational information provided
        through the platform or from temporary interruption or
        unavailability of the service.
      </p>

      <p>
        Nothing in these Terms of Use excludes or limits liability where
        doing so would be unlawful.
      </p>
    `
  },

  {
    id: 'privacy',
    num: '11',
    title: 'Privacy and Cookies',
    body: `
      <p>
        Personal information provided to AIWise is handled in accordance
        with our Privacy Policy.
      </p>

      <p>
        AIWise also uses essential technologies required to provide
        functionality such as authentication and maintaining user sessions.
        Further information is available in our Cookie Notice.
      </p>
    `
  },

  {
    id: 'changes',
    num: '12',
    title: 'Changes to These Terms',
    body: `
      <p>
        These Terms of Use may be updated when AIWise features, policies or
        applicable requirements change.
      </p>

      <p>
        When these Terms are updated, the "Last updated" date displayed on
        this page will also be changed.
      </p>
    `
  }
]

function scrollTo(id) {
  document
    .getElementById(id)
    ?.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    })

  activeSection.value = id
}

function onScroll() {
  const allIds = [
    ...sections.map(section => section.id),
    'contact-us'
  ]

  for (const id of [...allIds].reverse()) {
    const el = document.getElementById(id)

    if (el && el.getBoundingClientRect().top <= 120) {
      activeSection.value = id
      break
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, {
    passive: true
  })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.policy-page {
  min-height: 100vh;
  background: #fafaf8;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Nav */
.policy-nav {
  position: sticky;
  top: 0;
  z-index: 10;

  background: #fff;
  border-bottom: 1px solid #e5e5e5;

  padding: 0 40px;
  height: 58px;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-weight: 900;
  font-size: 20px;

  color: #3730a3;
  text-decoration: none;

  letter-spacing: -0.5px;
}

.nav-cta {
  background: #3730a3;
  color: #fff;

  border-radius: 8px;

  padding: 8px 18px;

  font-size: 13px;
  font-weight: 700;

  text-decoration: none;

  transition: background 0.15s;
}

.nav-cta:hover {
  background: #312e81;
}

/* Layout */
.policy-layout {
  max-width: 1100px;

  margin: 0 auto;
  padding: 0 40px 80px;

  display: grid;
  grid-template-columns: 220px 1fr;

  gap: 64px;

  align-items: start;
}

/* Table of contents */
.toc {
  position: sticky;
  top: 80px;

  padding-top: 56px;
}

.toc-inner {
  display: flex;
  flex-direction: column;
}

.toc-heading {
  font-size: 11px;
  font-weight: 700;

  letter-spacing: 1.5px;
  text-transform: uppercase;

  color: #aaa;

  margin: 0 0 14px;
}

.toc-link {
  display: block;

  font-size: 13px;
  font-weight: 500;

  color: #888;

  text-decoration: none;

  padding: 7px 0 7px 12px;

  border-left: 2px solid transparent;

  transition: all 0.15s;

  line-height: 1.4;
}

.toc-link:hover {
  color: #3730a3;
}

.toc-link--active {
  color: #3730a3;

  border-left-color: #3730a3;

  font-weight: 600;
}

.toc-contact {
  margin-top: 32px;
  padding-top: 20px;

  border-top: 1px solid #e5e5e5;
}

.toc-contact-label {
  font-size: 11px;
  font-weight: 700;

  letter-spacing: 1px;
  text-transform: uppercase;

  color: #aaa;

  margin: 0 0 6px;
}

.toc-email {
  font-size: 12px;
  font-weight: 600;

  color: #3730a3;

  text-decoration: none;

  word-break: break-all;
}

.toc-email:hover {
  text-decoration: underline;
}

/* Content */
.policy-content {
  padding-top: 56px;
}

/* Hero */
.policy-hero {
  margin-bottom: 56px;
}

.policy-badge {
  display: inline-block;

  font-size: 11px;
  font-weight: 700;

  letter-spacing: 1.5px;
  text-transform: uppercase;

  color: #6366f1;
  background: #eef2ff;

  padding: 4px 12px;

  border-radius: 20px;

  margin-bottom: 16px;
}

h1 {
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 900;

  color: #1e1b4b;

  letter-spacing: -1.5px;
  line-height: 1.1;

  margin: 0 0 20px;
}

.policy-intro {
  font-size: 17px;

  color: #555;

  line-height: 1.7;

  margin: 0 0 24px;

  max-width: 600px;
}

.policy-meta {
  display: flex;

  gap: 24px;

  flex-wrap: wrap;
}

.meta-item {
  display: flex;

  align-items: center;

  gap: 6px;

  font-size: 13px;

  color: #888;
}

.meta-icon {
  font-size: 14px;
}

/* Sections */
.policy-section {
  padding: 40px 0;

  border-top: 1px solid #e5e5e5;

  scroll-margin-top: 80px;
}

.section-num {
  font-size: 11px;
  font-weight: 800;

  letter-spacing: 2px;
  text-transform: uppercase;

  color: #d1d5db;

  margin-bottom: 10px;
}

.policy-section h2 {
  font-size: 22px;
  font-weight: 800;

  color: #1e1b4b;

  letter-spacing: -0.3px;

  margin: 0 0 18px;
}

.section-body {
  font-size: 15px;

  color: #555;

  line-height: 1.75;
}

.section-body :deep(p) {
  margin: 0 0 14px;
}

.section-body :deep(p:last-child) {
  margin-bottom: 0;
}

.section-body :deep(ul) {
  margin: 0;
  padding-left: 0;

  list-style: none;

  display: flex;
  flex-direction: column;

  gap: 10px;
}

.section-body :deep(li) {
  display: flex;

  align-items: flex-start;

  gap: 10px;

  padding: 12px 16px;

  background: #f9f9ff;

  border: 1px solid #ede9fe;

  border-radius: 8px;

  font-size: 14px;

  color: #444;

  line-height: 1.5;
}

.section-body :deep(li)::before {
  content: '→';

  color: #6366f1;

  font-weight: 700;

  flex-shrink: 0;

  margin-top: 1px;
}

.section-body :deep(strong) {
  color: #1e1b4b;
}

/* Contact */
.contact-section p {
  font-size: 15px;

  color: #555;

  line-height: 1.7;

  margin: 0 0 20px;
}

.contact-card {
  display: flex;

  align-items: center;

  gap: 16px;

  background: #1e1b4b;

  border-radius: 12px;

  padding: 20px 24px;

  text-decoration: none;

  transition: background 0.15s;
}

.contact-card:hover {
  background: #2d2a6e;
}

.contact-icon {
  width: 44px;
  height: 44px;

  background: rgba(255, 255, 255, 0.1);

  border-radius: 10px;

  display: flex;

  align-items: center;
  justify-content: center;

  font-size: 20px;

  flex-shrink: 0;
}

.contact-label {
  font-size: 12px;

  color: #a5b4fc;

  font-weight: 600;

  margin-bottom: 3px;
}

.contact-email {
  font-size: 15px;

  color: #fff;

  font-weight: 700;
}

.contact-arrow {
  margin-left: auto;

  font-size: 20px;

  color: #a5b4fc;
}

/* Footer note */
.policy-footer-note {
  margin-top: 48px;

  padding: 20px 24px;

  background: #f5f3ff;

  border: 1px solid #ede9fe;

  border-radius: 10px;

  font-size: 13px;

  color: #666;

  line-height: 1.6;
}

@media (max-width: 900px) {
  .policy-layout {
    grid-template-columns: 1fr;

    padding: 0 20px 60px;
  }

  .toc {
    display: none;
  }

  .policy-nav {
    padding: 0 20px;
  }
}
</style>