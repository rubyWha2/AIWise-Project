import { describe, expect, test, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import DashboardPage from '../src/views/DashboardPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  apiGet: vi.fn(),
}))

vi.mock('../src/services/api', () => ({
  default: { get: mocks.apiGet },
}))

describe('DashboardPage', () => {
  beforeEach(() => {
    mocks.apiGet.mockReset()
    mocks.apiGet.mockImplementation((url: string) => {
      if (url === '/loadDetails') return Promise.resolve({ data: { username: 'admin1', email: 'admin@aiwise.com' } })
      if (url === '/loadResults') {
        return Promise.resolve({
          data: [
            {
              result_id: 1,
              article_title: 'What Is Data Handling in Business?',
              created_at: '2026-09-09T10:00:00Z',
              score: 4,
              max_score: 5,
            },
          ],
        })
      }
      return Promise.resolve({ data: [] })
    })
  })

  test('loads the signed-in user and recent quiz activity', async () => {
    const wrapper = mountPage(DashboardPage)
    await flushPromises()

    expect(mocks.apiGet).toHaveBeenCalledWith('/loadDetails')
    expect(mocks.apiGet).toHaveBeenCalledWith('/loadResults')
    expect(wrapper.text()).toContain('admin1')
    expect(wrapper.text()).toContain('Quiz: What Is Data Handling in Business?')
    expect(wrapper.text()).toContain('80%')
  })

  test('shows external article suggestions', () => {
    const wrapper = mountPage(DashboardPage)

    // Suggestions are static frontend content, so this test just protects the visible section.
    expect(wrapper.text()).toContain('External articles we think you should read')
    expect(wrapper.text()).toContain('How AI is changing data protection')
  })
})
