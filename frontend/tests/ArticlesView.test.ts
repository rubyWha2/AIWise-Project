import { describe, expect, test, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import ArticlesView from '../src/views/ArticlesView.vue'
import { mountPage } from './test-utils'

const articles = [
  {
    article_id: 1,
    category: 'Data Protection',
    content: '<p>Data handling content</p>',
    title: 'What Is Data Handling in Business?',
  },
  {
    article_id: 6,
    category: 'AI',
    content: '<p>AI content</p>',
    title: 'Introduction to AI in Business',
  },
]

const mocks = vi.hoisted(() => ({
  apiGet: vi.fn(),
}))

vi.mock('../src/services/api', () => ({
  default: { get: mocks.apiGet },
}))

describe('ArticlesView', () => {
  beforeEach(() => {
    mocks.apiGet.mockReset()
    mocks.apiGet.mockImplementation((url: string) => {
      if (url === '/articles') return Promise.resolve({ data: articles })
      if (url === '/loadDetails') return Promise.resolve({ data: { username: 'admin1', email: 'admin@aiwise.com' } })
      return Promise.resolve({ data: [] })
    })
  })

  test('loads and renders article cards from the API', async () => {
    const wrapper = mountPage(ArticlesView)
    await flushPromises()

    expect(mocks.apiGet).toHaveBeenCalledWith('/articles')
    expect(wrapper.text()).toContain('What Is Data Handling in Business?')
    expect(wrapper.text()).toContain('Introduction to AI in Business')
  })

  test('filters articles by search text', async () => {
    const wrapper = mountPage(ArticlesView)
    await flushPromises()

    // The search input filters the already-loaded article list on the client.
    await wrapper.find('.search-input').setValue('data handling')

    expect(wrapper.text()).toContain('What Is Data Handling in Business?')
    expect(wrapper.text()).not.toContain('Introduction to AI in Business')
  })
})
