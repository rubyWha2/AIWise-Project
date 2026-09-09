import { describe, expect, test, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import LoginPage from '../src/views/LoginPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  push: vi.fn(),
  executeRecaptcha: vi.fn(),
  apiPost: vi.fn(),
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: mocks.push }),
}))

vi.mock('vue-recaptcha-v3', () => ({
  useReCaptcha: () => ({
    recaptchaLoaded: vi.fn().mockResolvedValue(undefined),
    executeRecaptcha: mocks.executeRecaptcha,
  }),
}))

vi.mock('../src/services/api', () => ({
  default: { post: mocks.apiPost },
}))

describe('LoginPage', () => {
  beforeEach(() => {
    mocks.push.mockReset()
    mocks.executeRecaptcha.mockReset().mockResolvedValue('recaptcha-token')
    mocks.apiPost.mockReset()
  })

  test('renders the login fields and links', () => {
    const wrapper = mountPage(LoginPage)

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('a[href="/forgot-password"]').text()).toContain('Forgot password')
    expect(wrapper.find('a[href="/register"]').text()).toContain('Create one')
  })

  test('shows validation messages when submitted empty', async () => {
    const wrapper = mountPage(LoginPage)

    await wrapper.find('form').trigger('submit')

    expect(wrapper.text()).toContain('Email is required.')
    expect(wrapper.text()).toContain('Password is required.')
    expect(mocks.apiPost).not.toHaveBeenCalled()
  })

  test('logs in with valid credentials and moves to dashboard', async () => {
    mocks.apiPost.mockResolvedValue({ data: { message: 'Login successful' } })
    const wrapper = mountPage(LoginPage)

    // The test fills the same v-model inputs a user would type into.
    await wrapper.find('#email').setValue('admin@aiwise.com')
    await wrapper.find('#password').setValue('wJ@x94pgW3LUmYU')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(mocks.apiPost).toHaveBeenCalledWith('/login', {
      email: 'admin@aiwise.com',
      password: 'wJ@x94pgW3LUmYU',
      recaptchaToken: 'recaptcha-token',
    })
    expect(mocks.push).toHaveBeenCalledWith('/dashboard')
  })
})
