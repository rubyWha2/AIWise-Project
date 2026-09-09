import { describe, expect, test, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import AccountPage from '../src/views/AccountPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  push: vi.fn(),
  apiGet: vi.fn(),
  apiPost: vi.fn(),
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: mocks.push }),
}))

vi.mock('../src/services/api', () => ({
  default: { get: mocks.apiGet, post: mocks.apiPost },
}))

describe('AccountPage', () => {
  beforeEach(() => {
    localStorage.clear()
    sessionStorage.clear()
    mocks.push.mockReset()
    mocks.apiPost.mockReset().mockResolvedValue({ data: { message: 'ok' } })
    mocks.apiGet.mockReset()
    mocks.apiGet.mockImplementation((url: string) => {
      if (url === '/loadDetails') return Promise.resolve({ data: { username: 'admin1', email: 'admin@aiwise.com' } })
      if (url === '/getAdminStatus') return Promise.resolve({ data: { user_id: 1, role_id: 1 } })
      return Promise.resolve({ data: {} })
    })
  })

  test('loads account details and shows the admin navigation link', async () => {
    const wrapper = mountPage(AccountPage)
    await flushPromises()

    expect(mocks.apiGet).toHaveBeenCalledWith('/loadDetails')
    expect(wrapper.text()).toContain('admin1')
    expect(wrapper.find('a[href="/admin"]').exists()).toBe(true)
  })

  test('logs out through the API and returns to landing', async () => {
    localStorage.setItem('example', 'value')
    sessionStorage.setItem('example', 'value')
    const wrapper = mountPage(AccountPage)
    await flushPromises()

    // Logout should clear browser storage only after the backend session call succeeds.
    await wrapper.find('.logout-btn').trigger('click')
    await flushPromises()

    expect(mocks.apiPost).toHaveBeenCalledWith('/logout')
    expect(localStorage.getItem('example')).toBeNull()
    expect(sessionStorage.getItem('example')).toBeNull()
    expect(mocks.push).toHaveBeenCalledWith('/')
  })

  test('opens the delete account confirmation modal', async () => {
    const wrapper = mountPage(AccountPage)
    await flushPromises()

    const dangerTab = wrapper.findAll('.tab-btn').find(button => button.text() === 'Danger zone')
    await dangerTab?.trigger('click')
    await wrapper.find('.btn-danger').trigger('click')

    expect(wrapper.text()).toContain('Enter your email to permanently delete your account.')
    expect(wrapper.find('.modal-backdrop').exists()).toBe(true)
  })
})
