import { describe, expect, test, vi } from 'vitest'
import SummaryPage from '../src/views/SummaryPage.vue'
import { mountPage } from './test-utils'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    query: {
      correct: '4',
      maxScore: '5',
      totalTime: '100',
    },
  }),
}))

vi.mock('../src/services/api', () => ({
  default: {},
}))

describe('SummaryPage', () => {
  test('calculates and displays the quiz result summary', () => {
    const wrapper = mountPage(SummaryPage)

    expect(wrapper.text()).toContain('80%')
    expect(wrapper.text()).toContain('4/5 correct')
    expect(wrapper.text()).toContain('20s')
    expect(wrapper.text()).toContain('+80 XP')
  })

  test('renders follow-up links for learning again', () => {
    const wrapper = mountPage(SummaryPage)

    // Router links are stubbed as anchors so the test checks the route targets directly.
    expect(wrapper.find('a[href="/articles"]').text()).toContain('Browse more articles')
    expect(wrapper.find('a[href="/quiz"]').text()).toContain('Retry quiz')
  })
})
