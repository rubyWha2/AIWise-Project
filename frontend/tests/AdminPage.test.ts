import { describe, expect, test, vi, beforeEach, afterEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import AdminPage from '../src/views/AdminPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  apiGet: vi.fn(),
  apiPut: vi.fn(),
  apiDelete: vi.fn(),
}))

vi.mock('../src/services/api', () => ({
  default: { get: mocks.apiGet, put: mocks.apiPut, delete: mocks.apiDelete },
}))

describe('AdminPage', () => {
  beforeEach(() => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    mocks.apiPut.mockReset().mockResolvedValue({ data: { message: 'User banned successfully' } })
    mocks.apiDelete.mockReset().mockResolvedValue({ data: { message: 'Deleted' } })
    mocks.apiGet.mockReset()
    mocks.apiGet.mockImplementation((url: string) => {
      if (url === '/count_all') return Promise.resolve({ data: { users: 2, articles: 1, quizzes_taken: 3, questions: 4 } })
      if (url === '/getTop6users') return Promise.resolve({ data: [{ username: 'admin1', email: 'admin@aiwise.com', created_at: '2026-09-09' }] })
      if (url === '/quizzes') return Promise.resolve({ data: [{ quiz_id: 1, question: 'What is data handling?', title: 'What Is Data Handling in Business?' }] })
      if (url === '/articles') return Promise.resolve({ data: [{ article_id: 1, title: 'What Is Data Handling in Business?', category: 'Data Protection' }] })
      if (url === '/users') return Promise.resolve({ data: [{ user_id: 2, username: 'learner1', email: 'learner@example.com', role_id: 2, created_at: '2026-09-09', banned: false }] })
      return Promise.resolve({ data: [] })
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  test('loads overview totals and recent users', async () => {
    const wrapper = mountPage(AdminPage)
    await flushPromises()

    expect(wrapper.text()).toContain('Recent signups')
    expect(wrapper.text()).toContain('admin1')
    expect(wrapper.text()).toContain('Quizzes taken')
  })

  test('filters articles in the articles section', async () => {
    const wrapper = mountPage(AdminPage)
    await flushPromises()

    const articlesButton = wrapper.findAll('.nav-item').find(button => button.text().includes('Articles'))
    await articlesButton?.trigger('click')
    await wrapper.find('.search-input').setValue('data handling')

    // The article tab uses API-loaded data and filters it locally.
    expect(wrapper.text()).toContain('What Is Data Handling in Business?')
  })

  test('bans a user from the users section', async () => {
    const wrapper = mountPage(AdminPage)
    await flushPromises()

    const usersButton = wrapper.findAll('.nav-item').find(button => button.text().includes('Users'))
    await usersButton?.trigger('click')
    await wrapper.find('.row-btn--danger').trigger('click')
    await flushPromises()

    expect(window.confirm).toHaveBeenCalledWith('Ban learner1?')
    expect(mocks.apiPut).toHaveBeenCalledWith('/users/2/ban')
  })

  test('deletes a quiz question from the quiz section', async () => {
    const wrapper = mountPage(AdminPage)
    await flushPromises()

    const quizButton = wrapper.findAll('.nav-item').find(button => button.text().includes('Quiz questions'))
    await quizButton?.trigger('click')
    await wrapper.find('.row-btn--danger').trigger('click')
    await flushPromises()

    expect(mocks.apiDelete).toHaveBeenCalledWith('/quizzes/1')
  })
})
