import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import './assets/styles.css'


;(function initTheme() {
  try {
    const saved = localStorage.getItem('theme')
    if (saved === 'light' || saved === 'dark') {
      document.documentElement.dataset.theme = saved
      return
    }
  } catch {}

  const prefersLight =
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: light)').matches

  document.documentElement.dataset.theme = prefersLight ? 'light' : 'dark'
})()

createApp(App).use(router).mount('#app')
