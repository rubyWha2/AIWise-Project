import { describe, expect, test, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import RegisterPage from '../src/views/RegisterPage.vue'
import { mountPage } from './test-utils'

const mocks = vi.hoisted(() => ({
  push: vi.fn(),
  apiPost: vi.fn(),
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: mocks.push }),
}))

vi.mock('../src/services/api', () => ({
  default: { post: mocks.apiPost },
}))

describe('RegisterPage', () => {
  beforeEach(() => {
    mocks.push.mockReset()
    mocks.apiPost.mockReset()
  })

  test('renders account fields and legal links', () => {
    const wrapper = mountPage(RegisterPage)

    expect(wrapper.find('#firstName').exists()).toBe(true)
    expect(wrapper.find('#lastName').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('a[href="/Terms"]').text()).toContain('Terms of Use')
    expect(wrapper.find('a[href="/Privacy"]').text()).toContain('Privacy Policy')
  })

  test('shows validation when required fields are missing', async () => {
    const wrapper = mountPage(RegisterPage)

    await wrapper.find('form').trigger('submit')

    expect(wrapper.text()).toContain('Required.')
    expect(wrapper.text()).toContain('Email is required.')
    expect(wrapper.text()).toContain('Password is required.')
    expect(mocks.apiPost).not.toHaveBeenCalled()
  })

  test('submits a valid registration and routes to login', async () => {
    mocks.apiPost.mockResolvedValue({ data: { message: 'User registered successfully' } })
    const wrapper = mountPage(RegisterPage)

    // This mirrors a complete successful sign-up form.
    await wrapper.find('#firstName').setValue('Admin')
    await wrapper.find('#lastName').setValue('One')
    await wrapper.find('#email').setValue('admin@aiwise.com')
    await wrapper.find('#password').setValue('wJ@x94pgW3LUmYU')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(mocks.apiPost).toHaveBeenCalledWith('/register', {
      firstName: 'Admin',
      lastName: 'One',
      email: 'admin@aiwise.com',
      password: 'wJ@x94pgW3LUmYU',
    })
    expect(mocks.push).toHaveBeenCalledWith('/login')
  })
})
