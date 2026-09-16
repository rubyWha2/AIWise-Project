import { describe, expect, test, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import QuizPage from '../src/views/QuizPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  push: vi.fn(),
  apiGet: vi.fn(),
  apiPost: vi.fn(),
}))

vi.mock('vue-router', () => ({
  useRoute: () => ({ query: { articleId: '1' } }),
  useRouter: () => ({ push: mocks.push }),
}))

vi.mock('../src/services/api', () => ({
  default: { get: mocks.apiGet, post: mocks.apiPost },
}))

const quizQuestions = [
  {
    quiz_id: 1,
    article_id: 1,
    title: 'What Is Data Handling in Business?',
    question: 'What is data handling?',
    option_a: 'Collecting and managing data',
    option_b: 'Deleting all customer records',
    option_c: 'Ignoring stored information',
    option_d: 'Only printing spreadsheets',
    correct_answer: 'a',
  },
]

describe('QuizPage', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    mocks.push.mockReset()
    mocks.apiGet.mockReset().mockResolvedValue({ data: quizQuestions })
    mocks.apiPost.mockReset().mockResolvedValue({ data: { message: 'Result saved' } })
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  test('loads quiz questions for the selected article', async () => {
    const wrapper = mountPage(QuizPage)
    await flushPromises()

    expect(mocks.apiGet).toHaveBeenCalledWith('/quiz/1')
    expect(wrapper.text()).toContain('What is data handling?')
    expect(wrapper.text()).toContain('Collecting and managing data')
  })

  test('marks the selected correct answer', async () => {
    const wrapper = mountPage(QuizPage)
    await flushPromises()

    // Selecting the right option should reveal the success styling.
    await wrapper.findAll('.option')[0].trigger('click')

    expect(wrapper.findAll('.option')[0].classes()).toContain('option--correct')
    expect(wrapper.find('.btn-next').exists()).toBe(true)
  })

  test('saves the result and navigates to the summary page', async () => {
    const wrapper = mountPage(QuizPage)
    await flushPromises()

    await wrapper.findAll('.option')[0].trigger('click')
    await wrapper.find('.btn-next').trigger('click')
    await flushPromises()

    expect(mocks.apiPost).toHaveBeenCalledWith('/updateResults', {
      article_id: '1',
      score: 1,
      max_score: 1,
    })
    expect(mocks.push).toHaveBeenCalledWith({
      name: 'Summary',
      query: {
        correct: 1,
        maxScore: 1,
        articleId: '1',
      },
    })
  })
})
