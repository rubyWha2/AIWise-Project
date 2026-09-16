import { describe, expect, test, beforeEach } from 'vitest'
import { nextTick } from 'vue'
import LandingPage from '../src/views/LandingPage.vue'
import { mountPage } from './test-utils'

describe('LandingPage', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  test('renders the main landing page actions', () => {
    const wrapper = mountPage(LandingPage)

    expect(wrapper.text()).toContain('Read. Test.')
    expect(wrapper.find('a[href="/register"]').exists()).toBe(true)
    expect(wrapper.find('a[href="/login"]').exists()).toBe(true)
  })

  test('links to privacy and terms pages from the footer', () => {
    const wrapper = mountPage(LandingPage)

    expect(wrapper.find('a[href="/privacy"]').text()).toContain('Privacy')
    expect(wrapper.find('a[href="/Terms"]').text()).toContain('Terms of Service')
  })

  test('shows and accepts the cookie notice once', async () => {
    const wrapper = mountPage(LandingPage)
    await nextTick()

    expect(wrapper.text()).toContain('Cookies on AIWise')

    // Clicking the notice button records the decision in browser storage.
    await wrapper.find('.cookie-btn').trigger('click')

    expect(localStorage.getItem('cookieNoticeAccepted')).toBe('true')
    expect(wrapper.find('.cookie-overlay').exists()).toBe(false)
  })
})
