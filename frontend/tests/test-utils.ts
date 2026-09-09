import { mount } from '@vue/test-utils'

// RouterLink is replaced with a normal anchor so tests can inspect links without a real router.
export const routerLinkStub = {
  props: ['to'],
  template: '<a :href="to"><slot /></a>',
}

export function mountPage(component: any, options: any = {}) {
  return mount(component, {
    ...options,
    global: {
      ...(options.global || {}),
      stubs: {
        RouterLink: routerLinkStub,
        ...(options.global?.stubs || {}),
      },
    },
  })
}
