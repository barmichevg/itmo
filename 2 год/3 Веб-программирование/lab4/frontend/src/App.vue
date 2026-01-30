<script setup>
import { computed, onMounted, ref } from 'vue'

const theme = ref('dark')

function applyTheme(t) {
  theme.value = t
  document.documentElement.dataset.theme = t
  try {
    localStorage.setItem('theme', t)
  } catch {}
}

function toggleTheme() {
  applyTheme(theme.value === 'light' ? 'dark' : 'light')
}

const ariaLabel = computed(() =>
  theme.value === 'light'
    ? 'Переключить на тёмную тему'
    : 'Переключить на светлую тему'
)

const icon = computed(() => (theme.value === 'light' ? '🌙' : '☀️'))

onMounted(() => {
  let saved = null
  try {
    saved = localStorage.getItem('theme')
  } catch {}

  if (saved === 'light' || saved === 'dark') {
    applyTheme(saved)
    return
  }

  const prefersLight =
    typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: light)').matches

  applyTheme(prefersLight ? 'light' : 'dark')
})
</script>

<template>
  <button class="theme-btn" type="button" :aria-label="ariaLabel" @click="toggleTheme">
    <span aria-hidden="true">{{ icon }}</span>
  </button>

  <div class="container">
    <router-view />
  </div>
</template>
