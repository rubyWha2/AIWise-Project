/// <reference types="vite/client" />

// Allow TypeScript to understand Vue single-file component imports.
declare module '*.vue' {
  import type { DefineComponent } from 'vue'

  const component: DefineComponent<object, object, any>
  export default component
}
