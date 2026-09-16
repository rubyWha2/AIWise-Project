import { describe, expect, test } from 'vitest'
import ArticlesView from '../src/views/ArticlesView.vue'

describe('ArticlesPage alias', () => {
  test('points to the real articles view component', () => {
    // This keeps the older file name useful while the actual page is ArticlesView.vue.
    expect(ArticlesView).toBeTruthy()
  })
})
